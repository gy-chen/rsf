from rsf import parser


def test_parse(sample_wiktionary_xml_file_path):
    elements = parser.parse(sample_wiktionary_xml_file_path)

    # only try first 10000 entries
    for _ in range(10000):
        elem = next(elements)
        assert elem["id"] is not None
        assert elem["title"] is not None

