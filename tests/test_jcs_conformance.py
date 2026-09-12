from __future__ import annotations
import hashlib
from pathlib import Path
import pytest
from actools.contracts.canonical import canonical_json_bytes
from actools.contracts.configuration import parse_json_bytes
from actools.contracts.errors import CanonicalizationError
ROOT=Path(__file__).resolve().parents[1]; V=ROOT/'tests/fixtures/jcs/cyberphone'; N=('arrays','french','structures','unicode','values','weird')
SHA={
'input/arrays.json':'e503b6d71d1afa595b1c74b1016445c944cd89f90418066b23de1aeda7d17563','input/french.json':'03676a951cd8753ac62589f72eb2105cc782c33425418cfe1d517c111f6e5d5a','input/structures.json':'d66893805be1784116af50af3110d08766c70a6b4aad93374723f72346e7aaa6','input/unicode.json':'4621864e014d4a805a563f55b9ea20aba4a2d2dc09c7394f625496998c00702c','input/values.json':'c4a041b503d6bc236036ef44db4dac499272f60fc22c40dc3b7a54870ba6f1c3','input/weird.json':'a3a905266bd4a49a969274ea69baa14ee0c4af0ead926d6fa2b7612b4af75387','output/arrays.json':'099601b171cafed97c333f8878d68e7f8c8f795412adb34b2fdcf0e7c7beac42','output/french.json':'d99d0ebdcb0033cb858cfa830ae46bc0fb3309413b271f1da828c89901a27ed5','output/structures.json':'605f65004ec2db7692522a0852c22f1c989e036d547e88963d1a3143cf3195d5','output/unicode.json':'0d99aad92a125196ff887876643fd3206786a84ddce2cee52ba4ad256d2381d3','output/values.json':'2d5e01a318d0f0879ab568c4be289c8b1f64ef8921a53c6277d5e069978baacb','output/weird.json':'6af595a9aa80110b964b4de3f82a05fa6ae7423005019bacfa2620dddc4e94d1'}
SET='99ec46b9c79cd60a60315a78346a67d760ec59c0f528f053176feefb7957414b'
def test_vector_receipt_digests():
    lines=[]
    for side in ('input','output'):
        for name in N:
            rel=f'{side}/{name}.json'; d=hashlib.sha256((V/rel).read_bytes()).hexdigest(); assert d==SHA[rel]; lines.append(f'{d}  {rel}\n')
    assert hashlib.sha256(''.join(lines).encode()).hexdigest()==SET
@pytest.mark.parametrize('name',N)
def test_published_pairs(name): assert canonical_json_bytes(parse_json_bytes((V/'input'/f'{name}.json').read_bytes()))==(V/'output'/f'{name}.json').read_bytes()
@pytest.mark.parametrize('raw,expected',[(b'0',b'0'),(b'-0',b'0'),(b'-0.0',b'0'),(b'4.50',b'4.5'),(b'2e-3',b'0.002'),(b'1e-7',b'1e-7'),(b'1e-6',b'0.000001'),(b'1e20',b'100000000000000000000'),(b'1e21',b'1e+21')])
def test_number_boundaries(raw,expected): assert canonical_json_bytes(parse_json_bytes(raw))==expected
def test_safe_integer_boundary():
    assert canonical_json_bytes(parse_json_bytes(b'9007199254740991'))==b'9007199254740991'
    with pytest.raises(Exception): parse_json_bytes(b'9007199254740992')
def test_canonical_rejects_nonfinite_surrogate_nonreflective():
    with pytest.raises(CanonicalizationError) as e: canonical_json_bytes(float('nan'))
    assert 'nan' not in str(e.value).lower()
    with pytest.raises(CanonicalizationError): canonical_json_bytes('\ud800')


def test_canonicalization_traceback_suppresses_underlying_rejected_value():
    import traceback

    rejected = 9_007_199_254_740_992
    try:
        canonical_json_bytes(rejected)
    except CanonicalizationError as exc:
        rendered = "".join(traceback.format_exception(exc))
        assert str(rejected) not in rendered
        assert exc.__cause__ is None
        assert exc.__suppress_context__ is True
    else:
        pytest.fail("out-of-domain integer unexpectedly canonicalized")
