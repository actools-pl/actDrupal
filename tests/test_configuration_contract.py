from __future__ import annotations
import copy, json
from pathlib import Path
import pytest
from actools.contracts.configuration import CONTRACT_VERSION, SUPPORTED_PROFILE, assert_schema_quality, load_configuration, parse_configuration_bytes, parse_json_bytes, parse_yaml_bytes, resolve_configuration
from actools.contracts.errors import ConfigurationError

ROOT=Path(__file__).resolve().parents[1]; FIX=ROOT/'tests/fixtures/configuration'
def rb(name:str)->bytes: return (FIX/name).read_bytes()
def minimal()->dict: return json.loads(rb('valid_minimal.json'))

def test_identity(): assert (CONTRACT_VERSION,SUPPORTED_PROFILE)==('1.0.0','single-site-production')
def test_equivalent_json_yaml_origins_and_jcs():
    j=load_configuration(rb('valid_minimal.json'),syntax='json'); y=load_configuration(rb('valid_minimal.yaml'),syntax='yaml')
    assert j.configuration==y.configuration; assert j.origins==y.origins
    assert j.canonical_configuration_bytes()==y.canonical_configuration_bytes(); assert j.canonical_resolution_bytes()==y.canonical_resolution_bytes()
def test_defaults_omission_only_origins_and_no_input_mutation():
    src=minimal(); before=copy.deepcopy(src); r=resolve_configuration(src); assert src==before
    assert r.configuration['platform']=={'os_profile':'ubuntu-26.04-amd64','runtime_backend':'docker-compose'}
    assert r.configuration['capabilities']['selected_ids']==[]
    assert r.origins['/platform/os_profile']=={'origin':'release_default','default_set':'configuration-defaults-1.0.0','default_set_version':'1.0.0'}
    assert r.origins['/site/domain']=={'origin':'operator'}
def test_null_false_empty_preserved():
    j=load_configuration(rb('valid_null_false.json'),syntax='json'); y=load_configuration(rb('valid_null_false.yaml'),syntax='yaml')
    assert j.configuration==y.configuration; assert j.origins==y.origins
    assert j.origins['/capabilities/selected_ids']=={'origin':'operator'}
    assert j.origins['/monitoring/notifications/email/enabled']=={'origin':'operator'}
    assert j.origins['/monitoring/notifications/email/secret_ref']=={'origin':'operator'}
def test_explicit_zero_not_defaulted():
    v=minimal(); v['recovery']={'rpo_minutes':0}
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert (e.value.path,e.value.reason)==('/recovery/rpo_minutes','value_out_of_range')
def test_origin_map_leaf_rule():
    r=resolve_configuration(minimal()); assert '' not in r.origins and '/installation' not in r.origins and '/capabilities/selected_ids' in r.origins

@pytest.mark.parametrize('name,syntax,reasons',[
 ('invalid_duplicate.json','json',{'duplicate_json_key'}),('invalid_duplicate.yaml','yaml',{'duplicate_yaml_key'}),
 ('invalid_ambiguous.yaml','yaml',{'yaml_ambiguous_scalar'}),('invalid_tag.yaml','yaml',{'yaml_tag_forbidden'}),
 ('invalid_merge.yaml','yaml',{'yaml_anchor_forbidden','yaml_alias_forbidden','yaml_merge_key_forbidden'}),
 ('invalid_alias.yaml','yaml',{'yaml_anchor_forbidden','yaml_alias_forbidden'}),('invalid_unknown.json','json',{'unknown_property'}),
 ('invalid_lone_surrogate.json','json',{'invalid_unicode_scalar'}),('invalid_nonfinite.json','json',{'nonfinite_json_constant'})])
def test_fixed_negatives(name,syntax,reasons):
    with pytest.raises(ConfigurationError) as e:
        v=parse_configuration_bytes(rb(name),syntax=syntax)
        if isinstance(v,dict): resolve_configuration(v)
    assert e.value.reason in reasons

def test_json_strict_failures_and_safe_bounds():
    cases=[(b'"\xff"','invalid_utf8'),(b'{} {}','invalid_json'),(b'{"x":Infinity}','nonfinite_json_constant'),(b'{"x":1e10000}','nonfinite_number'),(b'{"x":9007199254740992}','integer_outside_safe_range')]
    for raw,expected in cases:
        with pytest.raises(ConfigurationError) as e: parse_json_bytes(raw)
        assert e.value.reason==expected
    assert parse_json_bytes(b'{"x":9007199254740991}')["x"]==9007199254740991

@pytest.mark.parametrize('scalar,expected',[('null',None),('true',True),('false',False),('0',0),('-0',0),('1.25',1.25),('1e3',1000.0),('plain-text','plain-text'),('1.0.0','1.0.0'),('example.test','example.test')])
def test_yaml_accepted_plain_surface(scalar,expected): assert parse_yaml_bytes(f'value: {scalar}\n'.encode())=={'value':expected}
@pytest.mark.parametrize('scalar',['yes','No','ON','TRUE','Null','~','2026-09-11','2026-09-11T12:00:00Z','12:34:56','0x10','0o10','0b10','01','01.2','01e2','-01.2','1_000','1:20','.5','1.','+1','.nan','.inf','-.inf'])
def test_yaml_rejected_ambiguous_surface(scalar):
    with pytest.raises(ConfigurationError): parse_yaml_bytes(f'value: {scalar}\n'.encode())
def test_yaml_quoted_ambiguous_is_string(): assert parse_yaml_bytes(b'value: "yes"\n')=={'value':'yes'}
@pytest.mark.parametrize('raw,reason',[(b'value:\n','yaml_implicit_empty_null'),(b'value: |\n  text\n','yaml_scalar_style_forbidden'),(b'%YAML 1.2\n---\nvalue: text\n','yaml_directive_forbidden'),(b'---\nvalue: one\n---\nvalue: two\n','yaml_document_count'),(b'value: &a text\nother: *a\n','yaml_anchor_forbidden'),(b'value: !!str text\n','yaml_tag_forbidden'),(b'true: value\n','non_string_mapping_key'),(b'<<: {a: 1}\n','yaml_merge_key_forbidden'),(b'value: "\\uD800"\n','invalid_unicode_scalar'),(b'value: \xff\n','invalid_utf8')])
def test_yaml_structural_extensions(raw,reason):
    with pytest.raises(ConfigurationError) as e: parse_yaml_bytes(raw)
    assert e.value.reason==reason

def test_input_byte_limit_boundary():
    raw=b'{}'+b' '*(1_048_576-2); assert parse_json_bytes(raw)=={}
    with pytest.raises(ConfigurationError) as e: parse_json_bytes(raw+b' ')
    assert e.value.reason=='input_byte_limit'
def test_depth_boundary_root_level_one():
    v:object=0
    for _ in range(32): v=[v]
    assert parse_json_bytes(json.dumps(v).encode())==v
    with pytest.raises(ConfigurationError) as e: parse_json_bytes(json.dumps([v]).encode())
    assert e.value.reason=='container_depth_limit'
def test_mapping_and_sequence_boundaries():
    m={f'k{i}':0 for i in range(256)}; assert len(parse_json_bytes(json.dumps(m).encode()))==256
    m['overflow']=0
    with pytest.raises(ConfigurationError) as e: parse_json_bytes(json.dumps(m).encode())
    assert e.value.reason=='mapping_entry_limit'
    assert len(parse_json_bytes(json.dumps([0]*256).encode()))==256
    with pytest.raises(ConfigurationError) as e: parse_json_bytes(json.dumps([0]*257).encode())
    assert e.value.reason=='sequence_element_limit'
def test_aggregate_node_boundary():
    ok=[[0]*256 for _ in range(15)]+[[0]*239]; assert parse_json_bytes(json.dumps(ok).encode())==ok
    bad=[[0]*256 for _ in range(15)]+[[0]*240]
    with pytest.raises(ConfigurationError) as e: parse_json_bytes(json.dumps(bad).encode())
    assert e.value.reason=='aggregate_node_limit'
def test_string_boundary():
    assert len(parse_json_bytes(json.dumps('x'*16384).encode()))==16384
    with pytest.raises(ConfigurationError) as e: parse_json_bytes(json.dumps('x'*16385).encode())
    assert e.value.reason=='string_too_long'

@pytest.mark.parametrize('field,value,path',[('schema_version','2.0.0','/schema_version'),('profile','other','/profile')])
def test_unsupported_identity(field,value,path):
    v=minimal(); v[field]=value
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert e.value.path==path and e.value.reason.startswith('unsupported_')
def test_unknown_nested_property():
    v=minimal(); v['site']['unexpected']='x'
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert (e.value.path,e.value.reason)==('/site','unknown_property')
@pytest.mark.parametrize('mutator,path',[(lambda v:v['site'].update(domain='Example.COM'),'/site/domain'),(lambda v:v['host'].update(management_endpoint='bad endpoint'),'/host/management_endpoint'),(lambda v:v['host'].update(filesystem_authority_id='/srv/actools'),'/host/filesystem_authority_id'),(lambda v:v['secrets'].update(database_credentials='plaintext-password'),'/secrets/database_credentials')])
def test_owned_formats_asserted(mutator,path):
    v=minimal(); mutator(v)
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert (e.value.path,e.value.reason)==(path,'invalid_format')
def test_schema_files_do_not_use_json_schema_default_mutation():
    schema_dir=ROOT/'src/actools/contracts/schemas'
    def contains_default_keyword(value):
        if isinstance(value,dict):
            return 'default' in value or any(contains_default_keyword(v) for v in value.values())
        if isinstance(value,list):
            return any(contains_default_keyword(v) for v in value)
        return False
    for name in ('common-1.0.0.schema.json','configuration-1.0.0.schema.json'):
        assert not contains_default_keyword(json.loads((schema_dir/name).read_text(encoding='utf-8')))

def test_unregistered_schema_format_fails_quality():
    with pytest.raises(ConfigurationError) as e: assert_schema_quality({'$schema':'https://json-schema.org/draft/2020-12/schema','type':'string','format':'not-owned'})
    assert e.value.reason=='schema_unregistered_format'
def test_semantic_valid_capabilities_and_list_origins():
    v=minimal(); v['capabilities']={'selected_ids':['valkey-cache','cloudflare-standard-proxy']}; v['drupal']={'cache':{'mode':'valkey'},'ingress':{'mode':'cloudflare-standard'}}
    r=resolve_configuration(v); assert r.origins['/capabilities/selected_ids/0']=={'origin':'operator'}
def test_semantic_contradictions():
    v=minimal(); v['capabilities']={'selected_ids':['valkey-cache']}
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert e.value.reason=='valkey_capability_mismatch'
    v=minimal(); v['monitoring']={'notifications':{'email':{'enabled':True,'secret_ref':None}}}
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert e.value.reason=='enabled_channel_requires_secret_reference'
def test_secret_canary_not_reflected():
    canary='CP002_SECRET_CANARY_DO_NOT_PRINT'; v=minimal(); v['secrets']['database_credentials']=canary
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert canary not in str(e.value) and len(str(e.value))<160
def test_inline_secret_property_rejected_nonreflective():
    canary='CP002_SECRET_CANARY_DO_NOT_PRINT'; v=minimal(); v['secrets']['password']=canary
    with pytest.raises(ConfigurationError) as e: resolve_configuration(v)
    assert canary not in str(e.value) and e.value.reason=='unknown_property'
def test_envelope_detached():
    r=resolve_configuration(minimal()); e=r.resolution_envelope(); e['configuration']['site']['domain']='changed.invalid'; e['origins'].clear(); assert r.configuration['site']['domain']=='example.test' and r.origins
def test_zero_write_sentinel(tmp_path:Path,monkeypatch):
    sentinel=tmp_path/'sentinel'; sentinel.write_text('unchanged'); before={p.name:p.read_bytes() for p in tmp_path.iterdir()}
    def forbidden(*a,**k): raise AssertionError('write-capable pathlib operation reached')
    for name in ('write_text','write_bytes','mkdir','unlink','rename','replace','touch'): monkeypatch.setattr(Path,name,forbidden)
    assert load_configuration(rb('valid_minimal.json'),syntax='json').configuration['site']['domain']=='example.test'
    with pytest.raises(ConfigurationError): load_configuration(rb('invalid_duplicate.json'),syntax='json')
    after={p.name:p.read_bytes() for p in tmp_path.iterdir()}; assert after==before


def _leaf_pointers(value: object, parts: tuple[object, ...] = ()) -> set[str]:
    pointer = "" if not parts else "/" + "/".join(
        str(part).replace("~", "~0").replace("/", "~1") for part in parts
    )
    if isinstance(value, dict):
        if not value:
            return {pointer}
        result: set[str] = set()
        for key, child in value.items():
            result.update(_leaf_pointers(child, (*parts, key)))
        return result
    if isinstance(value, list):
        if not value:
            return {pointer}
        result: set[str] = set()
        for index, child in enumerate(value):
            result.update(_leaf_pointers(child, (*parts, index)))
        return result
    return {pointer}


def test_origin_map_exactly_covers_resolved_leaves_and_empty_containers():
    resolved = resolve_configuration(minimal())
    assert set(resolved.origins) == _leaf_pointers(resolved.configuration)
    for record in resolved.origins.values():
        assert record["origin"] in {"operator", "release_default"}
        if record["origin"] == "release_default":
            assert record == {
                "origin": "release_default",
                "default_set": "configuration-defaults-1.0.0",
                "default_set_version": "1.0.0",
            }
        else:
            assert record == {"origin": "operator"}


def _walk_schema_objects(value: object):
    if isinstance(value, dict):
        if value.get("type") == "object":
            yield value
        for child in value.values():
            yield from _walk_schema_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_schema_objects(child)


def test_owned_schema_is_closed_and_does_not_use_default_mutation_keyword():
    schema = json.loads(
        (ROOT / "src/actools/contracts/schemas/configuration-1.0.0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    common = json.loads(
        (ROOT / "src/actools/contracts/schemas/common-1.0.0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert '"default"' not in json.dumps(schema, sort_keys=True)
    assert all(item.get("additionalProperties") is False for item in _walk_schema_objects(schema))
    assert all(item.get("additionalProperties") is False for item in _walk_schema_objects(common))


@pytest.mark.parametrize(
    "selected,cache,ingress,reason",
    [
        (["valkey-cache"], "database", "direct-caddy", "valkey_capability_mismatch"),
        ([], "valkey", "direct-caddy", "valkey_capability_mismatch"),
        (["cloudflare-standard-proxy"], "database", "direct-caddy", "cloudflare_capability_mismatch"),
        ([], "database", "cloudflare-standard", "cloudflare_capability_mismatch"),
    ],
)
def test_capability_mode_contradictions_fail(selected, cache, ingress, reason):
    value = minimal()
    value["capabilities"] = {"selected_ids": selected}
    value["drupal"] = {"cache": {"mode": cache}, "ingress": {"mode": ingress}}
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert exc.value.reason == reason


@pytest.mark.parametrize("channel", ["email", "telegram"])
def test_enabled_notification_requires_secret_reference(channel):
    value = minimal()
    value["monitoring"] = {
        "notifications": {channel: {"enabled": True, "secret_ref": None}}
    }
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert exc.value.reason == "enabled_channel_requires_secret_reference"


@pytest.mark.parametrize("channel", ["email", "telegram"])
def test_disabled_notification_rejects_retained_secret_reference(channel):
    value = minimal()
    value["monitoring"] = {
        "notifications": {
            channel: {
                "enabled": False,
                "secret_ref": "secret://notifications/channel",
            }
        }
    }
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert exc.value.reason == "disabled_channel_forbids_secret_reference"


def test_configuration_module_has_no_effectful_runtime_imports():
    import ast

    source = (ROOT / "src/actools/contracts/configuration.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden = {"os", "subprocess", "socket", "urllib", "http", "requests"}
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id != "open"
    assert imports.isdisjoint(forbidden)


def test_explicit_null_and_empty_string_are_not_replaced_by_release_defaults():
    value = minimal()
    value["environment"]["type"] = None
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert (exc.value.path, exc.value.reason) == ("/environment/type", "unsupported_value")

    value = minimal()
    value["platform"] = {"os_profile": ""}
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert (exc.value.path, exc.value.reason) == ("/platform/os_profile", "unsupported_value")


def test_yaml_resource_boundaries_match_json_model_limits():
    nested: object = 0
    for _ in range(32):
        nested = [nested]
    assert parse_yaml_bytes(json.dumps(nested).encode("utf-8")) == nested
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(json.dumps([nested]).encode("utf-8"))
    assert exc.value.reason == "container_depth_limit"

    mapping = {f"k{i}": 0 for i in range(256)}
    assert len(parse_yaml_bytes(json.dumps(mapping).encode("utf-8"))) == 256
    mapping["overflow"] = 0
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(json.dumps(mapping).encode("utf-8"))
    assert exc.value.reason == "mapping_entry_limit"

    assert len(parse_yaml_bytes(json.dumps([0] * 256).encode("utf-8"))) == 256
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(json.dumps([0] * 257).encode("utf-8"))
    assert exc.value.reason == "sequence_element_limit"

    aggregate_ok = [[0] * 256 for _ in range(15)] + [[0] * 239]
    assert parse_yaml_bytes(json.dumps(aggregate_ok).encode("utf-8")) == aggregate_ok
    aggregate_bad = [[0] * 256 for _ in range(15)] + [[0] * 240]
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(json.dumps(aggregate_bad).encode("utf-8"))
    assert exc.value.reason == "aggregate_node_limit"

    assert parse_yaml_bytes(("value: \"" + "x" * 16_384 + "\"\n").encode("utf-8"))["value"] == "x" * 16_384
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(("value: \"" + "x" * 16_385 + "\"\n").encode("utf-8"))
    assert exc.value.reason == "string_too_long"


def test_yaml_input_byte_limit_is_checked_before_parser_work():
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(b"x" * (1_048_576 + 1))
    assert exc.value.reason == "input_byte_limit"


def test_integer_owned_fields_reject_integral_floats():
    value = minimal()
    value["recovery"] = {"rpo_minutes": 60.0}
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert (exc.value.path, exc.value.reason) == ("/recovery/rpo_minutes", "wrong_type")

    value = minimal()
    value["monitoring"] = {"health_interval_minutes": 5.0}
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert (exc.value.path, exc.value.reason) == ("/monitoring/health_interval_minutes", "wrong_type")


def test_traceback_output_suppresses_rejected_secret_canaries():
    import traceback

    canary = "CP002_TRACEBACK_SECRET_CANARY_DO_NOT_PRINT"
    raw_yaml = f"value: [{canary}\n".encode("utf-8")
    try:
        parse_yaml_bytes(raw_yaml)
    except ConfigurationError as exc:
        rendered = "".join(traceback.format_exception(exc))
        assert canary not in rendered
        assert exc.__cause__ is None
        assert exc.__suppress_context__ is True
    else:
        pytest.fail("malformed YAML unexpectedly accepted")

    raw_json = ("{\"value\":\"" + canary).encode("utf-8")
    try:
        parse_json_bytes(raw_json)
    except ConfigurationError as exc:
        rendered = "".join(traceback.format_exception(exc))
        assert canary not in rendered
        assert exc.__cause__ is None
        assert exc.__suppress_context__ is True
    else:
        pytest.fail("malformed JSON unexpectedly accepted")


def test_parser_error_paths_do_not_reflect_unowned_canary_keys():
    canary = "CP002_SECRET_CANARY_UNOWNED_KEY"
    with pytest.raises(ConfigurationError) as exc:
        parse_json_bytes(("{\"" + canary + "\":1e10000}").encode("utf-8"))
    assert exc.value.path == "/"
    assert canary not in str(exc.value)

    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes((canary + ": .nan\n").encode("utf-8"))
    assert exc.value.path == "/"
    assert canary not in str(exc.value)


def test_explicit_value_equal_to_release_default_remains_operator_origin():
    value = minimal()
    value["platform"] = {"os_profile": "ubuntu-26.04-amd64"}
    resolved = resolve_configuration(value)
    assert resolved.origins["/platform/os_profile"] == {"origin": "operator"}
    assert resolved.origins["/platform/runtime_backend"] == {
        "origin": "release_default",
        "default_set": "configuration-defaults-1.0.0",
        "default_set_version": "1.0.0",
    }


def test_required_field_errors_point_to_owned_missing_field():
    value = minimal()
    del value["installation"]
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert (exc.value.path, exc.value.reason) == ("/installation", "required_field_missing")

    value = minimal()
    del value["site"]["id"]
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert (exc.value.path, exc.value.reason) == ("/site/id", "required_field_missing")


def test_extreme_numeric_lexemes_fail_with_bounded_actools_reasons():
    huge_integer = b"9" * 10_000
    with pytest.raises(ConfigurationError) as exc:
        parse_json_bytes(huge_integer)
    assert exc.value.reason == "integer_outside_safe_range"
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(b"value: " + huge_integer + b"\n")
    assert exc.value.reason == "integer_outside_safe_range"

    huge_exponent = b"1e999999"
    with pytest.raises(ConfigurationError) as exc:
        parse_json_bytes(huge_exponent)
    assert exc.value.reason == "nonfinite_number"
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(b"value: " + huge_exponent + b"\n")
    assert exc.value.reason == "nonfinite_number"


def _encoded_document(value: dict, syntax: str) -> bytes:
    # JSON flow syntax is also valid YAML; using it here keeps all mutated
    # control-bearing strings explicitly quoted for the YAML-path assertions.
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


@pytest.mark.parametrize("syntax", ["json", "yaml"])
@pytest.mark.parametrize(
    "endpoint",
    [
        "[fe80::1%eth0]:22",
        "[fe80::1%bad\nzone]:22",
        "[fe80::1%bad\rzone]:22",
        "[fe80::1%bad\tzone]:22",
        "[fe80::1%bad\x1bzone]:22",
        "admin.example.test :22",
        "admin.example.test:\t22",
    ],
)
def test_ir01_scoped_or_control_bearing_endpoint_is_rejected_end_to_end(
    syntax: str, endpoint: str
) -> None:
    value = minimal()
    value["host"]["management_endpoint"] = endpoint
    with pytest.raises(ConfigurationError) as exc:
        load_configuration(_encoded_document(value, syntax), syntax=syntax)
    assert (exc.value.path, exc.value.reason) == (
        "/host/management_endpoint",
        "invalid_format",
    )
    assert endpoint not in str(exc.value)
    assert len(str(exc.value)) < 160


@pytest.mark.parametrize("syntax", ["json", "yaml"])
@pytest.mark.parametrize(
    "endpoint",
    [
        "admin.example.test:22",
        "192.0.2.10:1",
        "[2001:db8::1]:65535",
    ],
)
def test_ir01_unscoped_endpoint_forms_remain_valid(syntax: str, endpoint: str) -> None:
    value = minimal()
    value["host"]["management_endpoint"] = endpoint
    resolved = load_configuration(_encoded_document(value, syntax), syntax=syntax)
    assert resolved.configuration["host"]["management_endpoint"] == endpoint


_OWNED_SCALAR_CASES = [
    (("installation", "id"), "install-main"),
    (("site", "id"), "site-main"),
    (("environment", "id"), "production-main"),
    (("references", "policy"), "policy://single-site-production/1.0.0"),
    (("references", "release"), "release://actools/0.1.0-dev"),
]


def _set_path(value: dict, path: tuple[str, ...], replacement: str) -> None:
    current = value
    for part in path[:-1]:
        current = current[part]
    current[path[-1]] = replacement


@pytest.mark.parametrize("syntax", ["json", "yaml"])
@pytest.mark.parametrize("path,valid", _OWNED_SCALAR_CASES)
@pytest.mark.parametrize("suffix", ["\n", "\r", "\t", "\nextra"])
def test_ir02_owned_ids_and_references_require_true_end_of_string(
    syntax: str, path: tuple[str, ...], valid: str, suffix: str
) -> None:
    value = minimal()
    rejected = valid + suffix
    _set_path(value, path, rejected)
    with pytest.raises(ConfigurationError) as exc:
        load_configuration(_encoded_document(value, syntax), syntax=syntax)
    expected_path = "/" + "/".join(path)
    assert (exc.value.path, exc.value.reason) == (expected_path, "invalid_value_syntax")
    assert rejected not in str(exc.value)




def test_ir02_schema_patterns_use_ecmascript_compatible_true_end_construction() -> None:
    common = json.loads(
        (ROOT / "src/actools/contracts/schemas/common-1.0.0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    for name in ("identifier", "policyReference", "releaseReference"):
        pattern = common["$defs"][name]["pattern"]
        assert "\\Z" not in pattern
        assert pattern.endswith(r"(?![\s\S])")

@pytest.mark.parametrize("syntax", ["json", "yaml"])
def test_ir02_normal_owned_ids_and_references_still_validate(syntax: str) -> None:
    resolved = load_configuration(_encoded_document(minimal(), syntax), syntax=syntax)
    assert resolved.configuration["installation"]["id"] == "install-main"
    assert resolved.configuration["references"]["policy"].endswith("/1.0.0")


@pytest.mark.parametrize(
    "port_text,valid",
    [
        ("0", False),
        ("1", True),
        ("65535", True),
        ("65536", False),
        ("100000", False),
        ("01", False),
        ("١", False),
        ("9" * 4301, False),
        ("9" * 10000, False),
    ],
)
def test_ir03_endpoint_predicate_is_total_for_extreme_ports(
    port_text: str, valid: bool
) -> None:
    from actools.contracts.configuration import _is_endpoint

    assert _is_endpoint("127.0.0.1:" + port_text) is valid


@pytest.mark.parametrize("syntax", ["json", "yaml"])
@pytest.mark.parametrize(
    "port_text",
    ["0", "65536", "100000", "01", "١", "9" * 4301, "9" * 10000],
)
def test_ir03_invalid_ports_fail_with_owned_bounded_configuration_error(
    syntax: str, port_text: str
) -> None:
    value = minimal()
    endpoint = "127.0.0.1:" + port_text
    value["host"]["management_endpoint"] = endpoint
    with pytest.raises(ConfigurationError) as exc:
        load_configuration(_encoded_document(value, syntax), syntax=syntax)
    assert exc.value.path == "/host/management_endpoint"
    assert exc.value.reason in {"invalid_format", "value_out_of_range"}
    assert endpoint not in str(exc.value)
    assert len(str(exc.value)) < 160


@pytest.mark.parametrize("syntax", ["json", "yaml"])
@pytest.mark.parametrize("port_text", ["1", "65535"])
def test_ir03_port_boundaries_remain_valid(syntax: str, port_text: str) -> None:
    value = minimal()
    value["host"]["management_endpoint"] = "127.0.0.1:" + port_text
    resolved = load_configuration(_encoded_document(value, syntax), syntax=syntax)
    assert resolved.configuration["host"]["management_endpoint"].endswith(
        ":" + port_text
    )


def _pyyaml_plain_resolver_tags(text: str) -> set[str]:
    # Test oracle only. Production scalar meaning stays in _plain_yaml_scalar().
    from yaml.resolver import Resolver

    candidates = list(Resolver.yaml_implicit_resolvers.get(text[0], []))
    candidates.extend(Resolver.yaml_implicit_resolvers.get(None, []))
    return {tag for tag, pattern in candidates if pattern.match(text)}


@pytest.mark.parametrize(
    "scalar,reason,oracle_tag",
    [
        ("1.e+2", "yaml_numeric_extension", "tag:yaml.org,2002:float"),
        ("1.e-2", "yaml_numeric_extension", "tag:yaml.org,2002:float"),
        ("+1.e+2", "yaml_numeric_extension", "tag:yaml.org,2002:float"),
        ("-1.e+2", "yaml_numeric_extension", "tag:yaml.org,2002:float"),
        ("+1.e-2", "yaml_numeric_extension", "tag:yaml.org,2002:float"),
        ("-1.e-2", "yaml_numeric_extension", "tag:yaml.org,2002:float"),
        ("2026-9-11T12:00:00Z", "yaml_ambiguous_scalar", "tag:yaml.org,2002:timestamp"),
        ("2026-09-1T12:00:00Z", "yaml_ambiguous_scalar", "tag:yaml.org,2002:timestamp"),
        ("2026-9-1T12:00:00Z", "yaml_ambiguous_scalar", "tag:yaml.org,2002:timestamp"),
    ],
)
def test_ir04_pyyaml_ambiguity_oracle_is_rejected_but_quoted_form_is_string(
    scalar: str, reason: str, oracle_tag: str
) -> None:
    assert oracle_tag in _pyyaml_plain_resolver_tags(scalar)
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(f"value: {scalar}\n".encode("utf-8"))
    assert exc.value.reason == reason
    quoted = json.dumps(scalar).encode("utf-8")
    assert parse_yaml_bytes(b"value: " + quoted + b"\n") == {"value": scalar}


def _nested_list(levels: int) -> object:
    value: object = 0
    for _ in range(levels):
        value = [value]
    return value


def test_ir05_direct_mapping_depth_is_checked_before_recursive_copy() -> None:
    boundary = minimal()
    boundary["unexpected"] = _nested_list(31)
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(boundary)
    assert exc.value.reason == "unknown_property"
    assert "platform" not in boundary

    over_limit = minimal()
    deep_value = _nested_list(32)
    over_limit["unexpected"] = deep_value
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(over_limit)
    assert exc.value.reason == "container_depth_limit"
    assert over_limit["unexpected"] is deep_value
    assert "platform" not in over_limit

    far_over_limit = minimal()
    far_deep_value = _nested_list(1500)
    far_over_limit["unexpected"] = far_deep_value
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(far_over_limit)
    assert exc.value.reason == "container_depth_limit"
    assert far_over_limit["unexpected"] is far_deep_value
    assert "platform" not in far_over_limit


def test_ir05_direct_mapping_cycle_fails_owned_without_mutation() -> None:
    cyclic: list[object] = []
    cyclic.append(cyclic)
    value = minimal()
    value["unexpected"] = cyclic
    with pytest.raises(ConfigurationError) as exc:
        resolve_configuration(value)
    assert exc.value.reason == "container_depth_limit"
    assert value["unexpected"] is cyclic
    assert cyclic[0] is cyclic
    assert "platform" not in value


def test_ir04_non_resolved_one_digit_plain_date_remains_ordinary_text() -> None:
    scalar = "2026-9-11"
    assert _pyyaml_plain_resolver_tags(scalar) == set()
    assert parse_yaml_bytes(f"value: {scalar}\n".encode("utf-8")) == {"value": scalar}

@pytest.mark.parametrize(
    "scalar",
    [
        "2026-9-11TBD",
        "2026-9-11 Tomorrow",
        "2026-9-11T12:00:00Z-notes",
        "2026-9-11",
        "1.0.0",
    ],
)
def test_ir1_01_safe_date_prefixed_plain_text_remains_exact_string(scalar: str) -> None:
    assert _pyyaml_plain_resolver_tags(scalar) == set()
    assert parse_yaml_bytes(f"value: {scalar}\n".encode("utf-8")) == {"value": scalar}
    quoted = json.dumps(scalar).encode("utf-8")
    assert parse_yaml_bytes(b"value: " + quoted + b"\n") == {"value": scalar}


@pytest.mark.parametrize(
    "scalar",
    [
        "2026-9-11T12:00:00Z",
        "2026-09-1T12:00:00Z",
        "2026-9-1T12:00:00Z",
        "2026-9-11t12:00:00Z",
        "2026-9-11 12:00:00Z",
    ],
)
def test_ir1_01_true_timestamp_ambiguity_remains_rejected(scalar: str) -> None:
    assert "tag:yaml.org,2002:timestamp" in _pyyaml_plain_resolver_tags(scalar)
    with pytest.raises(ConfigurationError) as exc:
        parse_yaml_bytes(f"value: {scalar}\n".encode("utf-8"))
    assert exc.value.reason == "yaml_ambiguous_scalar"
    quoted = json.dumps(scalar).encode("utf-8")
    assert parse_yaml_bytes(b"value: " + quoted + b"\n") == {"value": scalar}

@pytest.mark.parametrize(
    "scalar,expected",
    [
        ("0", 0),
        ("-0", 0),
        ("0.0", 0.0),
        ("-0.1", -0.1),
        ("0e0", 0.0),
        ("0E+2", 0.0),
        ("1E-3", 0.001),
        ("-1.5e-2", -0.015),
    ],
)
def test_ir1_01_supported_json_number_lexemes_remain_supported(
    scalar: str, expected: int | float
) -> None:
    assert parse_yaml_bytes(f"value: {scalar}\n".encode("utf-8")) == {
        "value": expected
    }
