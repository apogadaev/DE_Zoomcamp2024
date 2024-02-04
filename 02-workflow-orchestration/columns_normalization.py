import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    pattern = re.compile(r'(?<=[a-z])_?(?=ID)')
    data.columns = [pattern.sub('_', col).lower() for col in data.columns]

    return data

@test
def test_output(output, *args) -> None:
    assert 'vendor_id' in output.columns
