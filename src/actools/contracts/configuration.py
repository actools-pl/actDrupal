"""Strict configuration parsing, validation, defaults and origin resolution."""
from __future__ import annotations
import copy, ipaddress, json, math, re
from collections.abc import Mapping
from dataclasses import dataclass
from importlib import resources
from typing import Any
import yaml
from jsonschema import Draft202012Validator, FormatChecker, validators
from yaml.events import AliasEvent, CollectionEndEvent, DocumentEndEvent, DocumentStartEvent, MappingEndEvent, MappingStartEvent, ScalarEvent, SequenceEndEvent, SequenceStartEvent, StreamEndEvent, StreamStartEvent
from yaml.tokens import AliasToken, AnchorToken, DirectiveToken, TagToken
from .canonical import MAX_AGGREGATE_NODES, MAX_CONTAINER_DEPTH, MAX_MAPPING_ENTRIES, MAX_SEQUENCE_ELEMENTS, MAX_STRING_SCALARS, SAFE_INTEGER_MAX, SAFE_INTEGER_MIN, canonical_json_bytes
from .errors import ConfigurationError
CONTRACT_VERSION = '1.0.0'
SUPPORTED_PROFILE = 'single-site-production'
DEFAULT_SET = 'configuration-defaults-1.0.0'
MAX_INPUT_BYTES = 1048576
_JSON_NUMBER = re.compile('-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\\Z')
_DOMAIN_LABEL = re.compile('[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\\Z')
_FS_AUTHORITY = re.compile('fs-auth:[a-z][a-z0-9-]{1,62}\\Z')
_SECRET_REFERENCE = re.compile('secret://[a-z][a-z0-9-]{0,62}/[a-z][a-z0-9-]{0,62}\\Z')
_DATE_LIKE = re.compile('(?:\\d{4}-\\d{2}-\\d{2}(?:[Tt ].*)?|\\d{4}-\\d{1,2}-\\d{1,2}[Tt ].*)\\Z')
_TIME_LIKE = re.compile('\\d{1,2}:\\d{2}:\\d{2}(?:\\.\\d+)?(?:[Zz]|[+-]\\d{2}:?\\d{2})?\\Z')
_SEXAGESIMAL = re.compile('[-+]?\\d+(?::[0-5]?\\d)+(?:\\.\\d+)?\\Z')
_NUMERIC_EXTENSION = re.compile('(?:[-+]?0[xX][0-9a-fA-F_]+|[-+]?0[oO][0-7_]+|[-+]?0[bB][01_]+|[-+]?0[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?|[-+]?\\.[0-9]+(?:[eE][+-]?[0-9]+)?|[-+]?[0-9]+\\.(?:[eE][+-]?[0-9]+)?|\\+[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)\\Z')
_AMBIGUOUS_WORDS = {'yes', 'no', 'on', 'off', 'y', 'n'}
_FORMAT_CHECKER = FormatChecker()
_FORMAT_CHECKER.checkers.clear()


def _native_integer_type(checker: object, instance: object) -> bool:
    del checker
    return isinstance(instance, int) and not isinstance(instance, bool)


_STRICT_TYPE_CHECKER = Draft202012Validator.TYPE_CHECKER.redefine(
    'integer', _native_integer_type
)
StrictDraft202012Validator = validators.extend(
    Draft202012Validator, type_checker=_STRICT_TYPE_CHECKER
)

def _is_domain(value: object) -> bool:
    if not isinstance(value, str) or len(value) > 253 or value.endswith('.'):
        return False
    labels = value.split('.')
    return len(labels) >= 2 and all((_DOMAIN_LABEL.fullmatch(label) for label in labels))

def _is_endpoint(value: object) -> bool:
    if not isinstance(value, str) or not value or len(value) > 320:
        return False
    if any(ch.isspace() or ord(ch) < 0x20 or ord(ch) == 0x7f for ch in value):
        return False
    if value.startswith('['):
        close = value.find(']')
        if close <= 1 or close + 1 >= len(value) or value[close + 1] != ':':
            return False
        host = value[1:close]
        port_text = value[close + 2:]
        if '%' in host:
            return False
        try:
            if ipaddress.ip_address(host).version != 6:
                return False
        except ValueError:
            return False
    else:
        if value.count(':') != 1:
            return False
        host, port_text = value.rsplit(':', 1)
        try:
            ipaddress.IPv4Address(host)
        except ValueError:
            if not _is_domain(host):
                return False
    if (
        not 1 <= len(port_text) <= 5
        or not port_text.isascii()
        or not port_text.isdigit()
        or (len(port_text) > 1 and port_text.startswith('0'))
    ):
        return False
    try:
        port = int(port_text)
    except (ValueError, OverflowError):
        return False
    return 1 <= port <= 65535

def _is_fs_authority(value: object) -> bool:
    return isinstance(value, str) and _FS_AUTHORITY.fullmatch(value) is not None

def _is_secret_reference(value: object) -> bool:
    return isinstance(value, str) and _SECRET_REFERENCE.fullmatch(value) is not None
_FORMAT_CHECKER.checks('actools-domain')(_is_domain)
_FORMAT_CHECKER.checks('actools-endpoint')(_is_endpoint)
_FORMAT_CHECKER.checks('actools-filesystem-authority-id')(_is_fs_authority)
_FORMAT_CHECKER.checks('actools-secret-reference')(_is_secret_reference)

def _pointer_escape(part: str) -> str:
    return part.replace('~', '~0').replace('/', '~1')

def _json_pointer(parts: list[object]) -> str:
    return '' if not parts else '/' + '/'.join((_pointer_escape(str(p)) for p in parts))


_OWNED_ERROR_PATH_SEGMENTS = {
    'schema_version', 'profile', 'installation', 'id', 'site', 'domain',
    'environment', 'type', 'platform', 'os_profile', 'runtime_backend',
    'capabilities', 'selected_ids', 'host', 'management_endpoint',
    'filesystem_authority_id', 'access', 'linux_administration',
    'privileged_drupal', 'editor', 'drupal', 'storage', 'public', 'private',
    'cache', 'mode', 'ingress', 'recovery', 'rpo_minutes', 'rto_minutes',
    'monitoring', 'health_interval_minutes', 'security_audit_interval_hours',
    'deep_diagnostic_interval_days', 'notifications', 'email', 'telegram',
    'enabled', 'secret_ref', 'secrets', 'database_credentials', 'references',
    'policy', 'release',
}


def _owned_error_path(parts: list[object]) -> str:
    for part in parts:
        if isinstance(part, int):
            continue
        if not isinstance(part, str) or part not in _OWNED_ERROR_PATH_SEGMENTS:
            return '/'
    pointer = _json_pointer(parts)
    return pointer or '/'

def _resource_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ConfigurationError('/', 'contract_resource_duplicate_key')
        result[key] = value
    return result


def _resource_constant(_: str) -> Any:
    raise ConfigurationError('/', 'contract_resource_nonfinite_number')


def _schema_resource(name: str) -> dict[str, Any]:
    try:
        raw = resources.files('actools.contracts').joinpath('schemas', name).read_bytes()
        text = raw.decode('utf-8', 'strict')
        value = json.loads(
            text,
            object_pairs_hook=_resource_pairs,
            parse_int=_json_integer,
            parse_float=_json_float,
            parse_constant=_resource_constant,
        )
    except ConfigurationError:
        raise
    except Exception as exc:
        raise ConfigurationError('/', 'schema_resource_unavailable') from None
    if not isinstance(value, dict):
        raise ConfigurationError('/', 'schema_resource_invalid')
    return value

def _known_formats(schema: Any) -> set[str]:
    found = set()
    if isinstance(schema, dict):
        if isinstance(schema.get('format'), str):
            found.add(schema['format'])
        for v in schema.values():
            found.update(_known_formats(v))
    elif isinstance(schema, list):
        for v in schema:
            found.update(_known_formats(v))
    return found

def assert_schema_quality(schema: Mapping[str, Any] | None=None) -> None:
    target = dict(schema) if schema is not None else _schema_resource('configuration-1.0.0.schema.json')
    try:
        Draft202012Validator.check_schema(target)
    except Exception as exc:
        raise ConfigurationError('/', 'schema_invalid') from None
    if _known_formats(target) - set(_FORMAT_CHECKER.checkers):
        raise ConfigurationError('/', 'schema_unregistered_format')

def _expand_common_refs(value: Any, common: Mapping[str, Any]) -> Any:
    if isinstance(value, dict):
        if set(value) == {'$ref'} and isinstance(value['$ref'], str):
            prefix = 'common-1.0.0.schema.json#/$defs/'
            if value['$ref'].startswith(prefix):
                name = value['$ref'][len(prefix):]
                definition = common.get('$defs', {}).get(name)
                if definition is None:
                    raise ConfigurationError('/', 'schema_reference_invalid')
                return _expand_common_refs(copy.deepcopy(definition), common)
        return {k: _expand_common_refs(v, common) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_common_refs(v, common) for v in value]
    return value

def _configuration_schema() -> dict[str, Any]:
    common = _schema_resource('common-1.0.0.schema.json')
    schema = _schema_resource('configuration-1.0.0.schema.json')
    expanded = _expand_common_refs(schema, common)
    assert_schema_quality(expanded)
    return expanded

def _valid_json_pointer(pointer: object) -> bool:
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        return False
    for token in pointer.split('/')[1:]:
        index = 0
        while index < len(token):
            if token[index] == '~':
                if index + 1 >= len(token) or token[index + 1] not in {'0', '1'}:
                    return False
                index += 2
            else:
                index += 1
    return True


def _defaults_document() -> dict[str, Any]:
    value = _schema_resource('configuration-defaults-1.0.0.json')
    if set(value) != {
        'schema_version',
        'profile',
        'default_set',
        'default_set_version',
        'defaults',
    }:
        raise ConfigurationError('/', 'default_set_invalid')
    if (
        value.get('schema_version') != CONTRACT_VERSION
        or value.get('profile') != SUPPORTED_PROFILE
        or value.get('default_set') != DEFAULT_SET
        or value.get('default_set_version') != CONTRACT_VERSION
    ):
        raise ConfigurationError('/', 'default_set_identity_mismatch')
    defaults = value.get('defaults')
    if not isinstance(defaults, dict) or not defaults:
        raise ConfigurationError('/', 'default_set_invalid')
    if not all(_valid_json_pointer(pointer) for pointer in defaults):
        raise ConfigurationError('/', 'default_set_pointer_invalid')
    _validate_data_limits(defaults)
    return value

def _validate_unicode(text: str, path: str) -> None:
    if len(text) > MAX_STRING_SCALARS:
        raise ConfigurationError(path, 'string_too_long')
    if any((55296 <= ord(ch) <= 57343 for ch in text)):
        raise ConfigurationError(path, 'invalid_unicode_scalar')

def _validate_data_limits(value: Any) -> None:
    nodes = 0

    def walk(item: Any, depth: int, parts: list[object]) -> None:
        nonlocal nodes
        path = _owned_error_path(parts)
        nodes += 1
        if nodes > MAX_AGGREGATE_NODES:
            raise ConfigurationError('/', 'aggregate_node_limit')
        if item is None or isinstance(item, bool):
            return
        if isinstance(item, int):
            if not SAFE_INTEGER_MIN <= item <= SAFE_INTEGER_MAX:
                raise ConfigurationError(path, 'integer_outside_safe_range')
            return
        if isinstance(item, float):
            if not math.isfinite(item):
                raise ConfigurationError(path, 'nonfinite_number')
            return
        if isinstance(item, str):
            _validate_unicode(item, path)
            return
        if isinstance(item, dict):
            nd = depth + 1
            if nd > MAX_CONTAINER_DEPTH:
                raise ConfigurationError(path, 'container_depth_limit')
            if len(item) > MAX_MAPPING_ENTRIES:
                raise ConfigurationError(path, 'mapping_entry_limit')
            for k, v in item.items():
                if not isinstance(k, str):
                    raise ConfigurationError(path, 'non_string_mapping_key')
                nodes += 1
                if nodes > MAX_AGGREGATE_NODES:
                    raise ConfigurationError('/', 'aggregate_node_limit')
                _validate_unicode(k, path)
                walk(v, nd, [*parts, k])
            return
        if isinstance(item, list):
            nd = depth + 1
            if nd > MAX_CONTAINER_DEPTH:
                raise ConfigurationError(path, 'container_depth_limit')
            if len(item) > MAX_SEQUENCE_ELEMENTS:
                raise ConfigurationError(path, 'sequence_element_limit')
            for i, v in enumerate(item):
                walk(v, nd, [*parts, i])
            return
        raise ConfigurationError(path, 'non_json_value')
    walk(value, 0, [])

def _json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for k, v in pairs:
        if k in result:
            raise ConfigurationError('/', 'duplicate_json_key')
        result[k] = v
    return result


def _parse_safe_integer_text(text: str, path: str) -> int:
    digits = text[1:] if text.startswith('-') else text
    if len(digits) > 16:
        raise ConfigurationError(path, 'integer_outside_safe_range')
    try:
        value = int(text)
    except (ValueError, OverflowError):
        raise ConfigurationError(path, 'integer_outside_safe_range') from None
    if not SAFE_INTEGER_MIN <= value <= SAFE_INTEGER_MAX:
        raise ConfigurationError(path, 'integer_outside_safe_range')
    return value


def _parse_finite_float_text(text: str, path: str) -> float:
    try:
        value = float(text)
    except (ValueError, OverflowError):
        raise ConfigurationError(path, 'nonfinite_number') from None
    if not math.isfinite(value):
        raise ConfigurationError(path, 'nonfinite_number')
    return value


def _json_integer(text: str) -> int:
    return _parse_safe_integer_text(text, '/')


def _json_float(text: str) -> float:
    return _parse_finite_float_text(text, '/')


def _json_constant(_: str) -> Any:
    raise ConfigurationError('/', 'nonfinite_json_constant')

def _precheck_json_depth(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for ch in text:
        if in_string:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in '[{':
            depth += 1
            if depth > MAX_CONTAINER_DEPTH:
                raise ConfigurationError('/', 'container_depth_limit')
        elif ch in ']}':
            depth -= 1

def parse_json_bytes(data: bytes) -> Any:
    if len(data) > MAX_INPUT_BYTES:
        raise ConfigurationError('/', 'input_byte_limit')
    try:
        text = data.decode('utf-8', 'strict')
    except UnicodeDecodeError as exc:
        raise ConfigurationError('/', 'invalid_utf8') from None
    _precheck_json_depth(text)
    try:
        value = json.loads(
            text,
            object_pairs_hook=_json_pairs,
            parse_int=_json_integer,
            parse_float=_json_float,
            parse_constant=_json_constant,
        )
    except ConfigurationError:
        raise
    except (json.JSONDecodeError, ValueError, OverflowError) as exc:
        raise ConfigurationError('/', 'invalid_json') from None
    _validate_data_limits(value)
    return value

def _plain_yaml_scalar(text: str, path: str) -> Any:
    if text == '':
        raise ConfigurationError(path, 'yaml_implicit_empty_null')
    if text == 'null':
        return None
    if text == 'true':
        return True
    if text == 'false':
        return False
    lower = text.lower()
    if lower in _AMBIGUOUS_WORDS or (lower in {'true', 'false', 'null'} and text != lower) or text == '~':
        raise ConfigurationError(path, 'yaml_ambiguous_scalar')
    if lower in {'.nan', '.inf', '+.inf', '-.inf'}:
        raise ConfigurationError(path, 'yaml_nonfinite_number')
    if _DATE_LIKE.fullmatch(text) or _TIME_LIKE.fullmatch(text) or _SEXAGESIMAL.fullmatch(text):
        raise ConfigurationError(path, 'yaml_ambiguous_scalar')
    if _NUMERIC_EXTENSION.fullmatch(text) or ('_' in text and re.match('[-+]?(?:\\d|\\.)', text)):
        raise ConfigurationError(path, 'yaml_numeric_extension')
    if _JSON_NUMBER.fullmatch(text):
        if any((ch in text for ch in '.eE')):
            return _parse_finite_float_text(text, path)
        return _parse_safe_integer_text(text, path)
    _validate_unicode(text, path)
    return text

def _yaml_scalar(event: ScalarEvent, path: str, *, mapping_key: bool=False) -> Any:
    if event.anchor is not None:
        raise ConfigurationError(path, 'yaml_anchor_forbidden')
    if event.tag is not None:
        raise ConfigurationError(path, 'yaml_tag_forbidden')
    if event.style in {'|', '>'}:
        raise ConfigurationError(path, 'yaml_scalar_style_forbidden')
    if event.style in {"'", '"'}:
        _validate_unicode(event.value, path)
        return event.value
    value = _plain_yaml_scalar(event.value, path)
    if mapping_key and (not isinstance(value, str)):
        raise ConfigurationError(path, 'non_string_mapping_key')
    return value

def _preflight_yaml(data: bytes) -> list[Any]:
    if len(data) > MAX_INPUT_BYTES:
        raise ConfigurationError('/', 'input_byte_limit')
    try:
        text = data.decode('utf-8', 'strict')
    except UnicodeDecodeError as exc:
        raise ConfigurationError('/', 'invalid_utf8') from None
    try:
        for token in yaml.scan(text):
            if isinstance(token, DirectiveToken):
                raise ConfigurationError('/', 'yaml_directive_forbidden')
            if isinstance(token, AnchorToken):
                raise ConfigurationError('/', 'yaml_anchor_forbidden')
            if isinstance(token, AliasToken):
                raise ConfigurationError('/', 'yaml_alias_forbidden')
            if isinstance(token, TagToken):
                raise ConfigurationError('/', 'yaml_tag_forbidden')
        events: list[Any] = []
        document_count = 0
        collection_depth = 0
        parsed_nodes = 0
        for event in yaml.parse(text):
            if isinstance(event, DocumentStartEvent):
                document_count += 1
                if document_count > 1:
                    raise ConfigurationError('/', 'yaml_document_count')
            if isinstance(event, (MappingStartEvent, SequenceStartEvent)):
                collection_depth += 1
                parsed_nodes += 1
                if collection_depth > MAX_CONTAINER_DEPTH:
                    raise ConfigurationError('/', 'container_depth_limit')
            elif isinstance(event, (MappingEndEvent, SequenceEndEvent)):
                collection_depth -= 1
            elif isinstance(event, ScalarEvent):
                parsed_nodes += 1
            if parsed_nodes > MAX_AGGREGATE_NODES:
                raise ConfigurationError('/', 'aggregate_node_limit')
            events.append(event)
    except ConfigurationError:
        raise
    except yaml.YAMLError as exc:
        raise ConfigurationError('/', 'invalid_yaml') from None
    if document_count != 1:
        raise ConfigurationError('/', 'yaml_document_count')
    return events

def parse_yaml_bytes(data: bytes) -> Any:
    events = _preflight_yaml(data)
    index = 0
    nodes = 0

    def take(expected=None):
        nonlocal index
        if index >= len(events):
            raise ConfigurationError('/', 'invalid_yaml_event_stream')
        event = events[index]
        if expected is not None and (not isinstance(event, expected)):
            raise ConfigurationError('/', 'invalid_yaml_event_stream')
        index += 1
        return event
    take(StreamStartEvent)
    take(DocumentStartEvent)

    def build(parts: list[object], depth: int) -> Any:
        nonlocal nodes, index
        if index >= len(events):
            raise ConfigurationError('/', 'invalid_yaml_event_stream')
        event = events[index]
        path = _owned_error_path(parts)
        nodes += 1
        if nodes > MAX_AGGREGATE_NODES:
            raise ConfigurationError('/', 'aggregate_node_limit')
        if isinstance(event, AliasEvent):
            raise ConfigurationError(path, 'yaml_alias_forbidden')
        if isinstance(event, ScalarEvent):
            index += 1
            return _yaml_scalar(event, path)
        if isinstance(event, MappingStartEvent):
            if event.anchor is not None:
                raise ConfigurationError(path, 'yaml_anchor_forbidden')
            if event.tag is not None:
                raise ConfigurationError(path, 'yaml_tag_forbidden')
            if depth + 1 > MAX_CONTAINER_DEPTH:
                raise ConfigurationError(path, 'container_depth_limit')
            index += 1
            result = {}
            while not isinstance(events[index], MappingEndEvent):
                if len(result) >= MAX_MAPPING_ENTRIES:
                    raise ConfigurationError(path, 'mapping_entry_limit')
                key_event = events[index]
                if not isinstance(key_event, ScalarEvent):
                    raise ConfigurationError(path, 'non_string_mapping_key')
                index += 1
                nodes += 1
                if nodes > MAX_AGGREGATE_NODES:
                    raise ConfigurationError('/', 'aggregate_node_limit')
                key = _yaml_scalar(key_event, path, mapping_key=True)
                if key_event.style is None and key == '<<':
                    raise ConfigurationError(path, 'yaml_merge_key_forbidden')
                if key in result:
                    raise ConfigurationError(path, 'duplicate_yaml_key')
                result[key] = build([*parts, key], depth + 1)
            index += 1
            return result
        if isinstance(event, SequenceStartEvent):
            if event.anchor is not None:
                raise ConfigurationError(path, 'yaml_anchor_forbidden')
            if event.tag is not None:
                raise ConfigurationError(path, 'yaml_tag_forbidden')
            if depth + 1 > MAX_CONTAINER_DEPTH:
                raise ConfigurationError(path, 'container_depth_limit')
            index += 1
            result = []
            while not isinstance(events[index], SequenceEndEvent):
                if len(result) >= MAX_SEQUENCE_ELEMENTS:
                    raise ConfigurationError(path, 'sequence_element_limit')
                result.append(build([*parts, len(result)], depth + 1))
            index += 1
            return result
        if isinstance(event, CollectionEndEvent):
            raise ConfigurationError(path, 'invalid_yaml_event_stream')
        raise ConfigurationError(path, 'yaml_event_forbidden')
    value = build([], 0)
    take(DocumentEndEvent)
    take(StreamEndEvent)
    if index != len(events):
        raise ConfigurationError('/', 'yaml_document_count')
    _validate_data_limits(value)
    return value

def parse_configuration_bytes(data: bytes, *, syntax: str) -> Any:
    if syntax == 'json':
        return parse_json_bytes(data)
    if syntax == 'yaml':
        return parse_yaml_bytes(data)
    raise ConfigurationError('/', 'unsupported_input_syntax')

def _prevalidate_identity(value: Any) -> None:
    if not isinstance(value, dict):
        raise ConfigurationError('/', 'root_must_be_object')
    if value.get('schema_version') != CONTRACT_VERSION:
        raise ConfigurationError('/schema_version', 'unsupported_schema_version')
    if value.get('profile') != SUPPORTED_PROFILE:
        raise ConfigurationError('/profile', 'unsupported_profile')

def _lookup_pointer(document: Any, pointer: str) -> tuple[bool, Any]:
    if pointer == '':
        return (True, document)
    current = document
    for encoded in pointer.split('/')[1:]:
        key = encoded.replace('~1', '/').replace('~0', '~')
        if isinstance(current, dict):
            if key not in current:
                return (False, None)
            current = current[key]
        elif isinstance(current, list) and key.isdigit():
            i = int(key)
            if i >= len(current):
                return (False, None)
            current = current[i]
        else:
            return (False, None)
    return (True, current)

def _set_pointer_if_omitted(document: dict[str, Any], pointer: str, value: Any) -> bool:
    parts = pointer.split('/')[1:]
    current = document
    for encoded in parts[:-1]:
        key = encoded.replace('~1', '/').replace('~0', '~')
        existing = current.get(key)
        if existing is None and key not in current:
            current[key] = {}
            existing = current[key]
        if not isinstance(existing, dict):
            return False
        current = existing
    leaf = parts[-1].replace('~1', '/').replace('~0', '~')
    if leaf in current:
        return False
    current[leaf] = copy.deepcopy(value)
    return True

def _apply_defaults(document: dict[str, Any]) -> set[str]:
    defaults = _defaults_document()['defaults']
    applied = set()
    for pointer in sorted(defaults):
        if _set_pointer_if_omitted(document, pointer, defaults[pointer]):
            applied.add(pointer)
    return applied

def _schema_reason(error: Any) -> str:
    return {'additionalProperties': 'unknown_property', 'required': 'required_field_missing', 'format': 'invalid_format', 'minimum': 'value_out_of_range', 'maximum': 'value_out_of_range', 'minLength': 'value_out_of_range', 'maxLength': 'value_out_of_range', 'minItems': 'value_out_of_range', 'maxItems': 'value_out_of_range', 'const': 'unsupported_value', 'enum': 'unsupported_value', 'type': 'wrong_type', 'uniqueItems': 'duplicate_array_value', 'pattern': 'invalid_value_syntax'}.get(getattr(error, 'validator', None), 'schema_validation_failed')

def _validate_schema(document: dict[str, Any]) -> None:
    validator = StrictDraft202012Validator(
        _configuration_schema(), format_checker=_FORMAT_CHECKER
    )
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: _json_pointer(list(error.absolute_path)),
    )
    if errors:
        e = errors[0]
        path_parts = list(e.absolute_path)
        if (
            e.validator == 'required'
            and isinstance(e.validator_value, list)
            and isinstance(e.instance, dict)
        ):
            missing = [name for name in e.validator_value if name not in e.instance]
            if missing:
                path_parts.append(missing[0])
        raise ConfigurationError(_json_pointer(path_parts), _schema_reason(e))

def _validate_semantics(document: dict[str, Any]) -> None:
    selected = set(document['capabilities']['selected_ids'])
    if (document['drupal']['cache']['mode'] == 'valkey') != ('valkey-cache' in selected):
        raise ConfigurationError('/drupal/cache/mode', 'valkey_capability_mismatch')
    if (document['drupal']['ingress']['mode'] == 'cloudflare-standard') != ('cloudflare-standard-proxy' in selected):
        raise ConfigurationError('/drupal/ingress/mode', 'cloudflare_capability_mismatch')
    for channel in ('email', 'telegram'):
        item = document['monitoring']['notifications'][channel]
        enabled = item['enabled']
        reference = item['secret_ref']
        if enabled and reference is None:
            raise ConfigurationError(f'/monitoring/notifications/{channel}/secret_ref', 'enabled_channel_requires_secret_reference')
        if not enabled and reference is not None:
            raise ConfigurationError(f'/monitoring/notifications/{channel}/secret_ref', 'disabled_channel_forbids_secret_reference')

def _collect_origins(document: Any, operator: Any, applied: set[str]) -> dict[str, dict[str, str]]:
    origins = {}

    def walk(item: Any, parts: list[object]) -> None:
        pointer = _json_pointer(parts)
        if isinstance(item, dict):
            if not item:
                present, _ = _lookup_pointer(operator, pointer)
                origin = 'operator' if present else 'release_default'
                record = {'origin': origin}
                if origin == 'release_default':
                    record.update({'default_set': DEFAULT_SET, 'default_set_version': CONTRACT_VERSION})
                origins[pointer] = record
            for k, v in item.items():
                walk(v, [*parts, k])
            return
        if isinstance(item, list):
            if not item:
                present, _ = _lookup_pointer(operator, pointer)
                origin = 'operator' if present else 'release_default'
                record = {'origin': origin}
                if origin == 'release_default':
                    record.update({'default_set': DEFAULT_SET, 'default_set_version': CONTRACT_VERSION})
                origins[pointer] = record
            else:
                for i, v in enumerate(item):
                    walk(v, [*parts, i])
            return
        present, _ = _lookup_pointer(operator, pointer)
        if present:
            origins[pointer] = {'origin': 'operator'}
        else:
            if not any((pointer == d or pointer.startswith(d + '/') for d in applied)):
                raise ConfigurationError(pointer, 'origin_source_unresolved')
            origins[pointer] = {'origin': 'release_default', 'default_set': DEFAULT_SET, 'default_set_version': CONTRACT_VERSION}
    walk(document, [])
    return {k: origins[k] for k in sorted(origins)}

@dataclass(frozen=True)
class ResolvedConfiguration:
    configuration: dict[str, Any]
    origins: dict[str, dict[str, str]]

    def canonical_configuration_bytes(self) -> bytes:
        return canonical_json_bytes(self.configuration)

    def resolution_envelope(self) -> dict[str, Any]:
        return {'configuration': copy.deepcopy(self.configuration), 'origins': copy.deepcopy(self.origins)}

    def canonical_resolution_bytes(self) -> bytes:
        return canonical_json_bytes(self.resolution_envelope())

def resolve_configuration(value: Mapping[str, Any]) -> ResolvedConfiguration:
    operator_input = dict(value)
    _validate_data_limits(operator_input)
    operator = copy.deepcopy(operator_input)
    _prevalidate_identity(operator)
    resolved = copy.deepcopy(operator)
    applied = _apply_defaults(resolved)
    _validate_data_limits(resolved)
    _validate_schema(resolved)
    _validate_semantics(resolved)
    origins = _collect_origins(resolved, operator, applied)
    return ResolvedConfiguration(copy.deepcopy(resolved), copy.deepcopy(origins))

def load_configuration(data: bytes, *, syntax: str) -> ResolvedConfiguration:
    parsed = parse_configuration_bytes(data, syntax=syntax)
    if not isinstance(parsed, dict):
        raise ConfigurationError('/', 'root_must_be_object')
    return resolve_configuration(parsed)
