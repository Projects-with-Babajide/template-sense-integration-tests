"""Basic import and version tests for template-sense package."""


def test_import_template_sense():
    """Test that template_sense package can be imported."""
    import template_sense

    assert template_sense is not None


def test_import_analyzer_service():
    """Test that AnalyzerService can be imported."""
    from template_sense.analyzer import extract_template_structure

    assert extract_template_structure is not None


def test_version_attribute_exists():
    """Test that package has a version attribute."""
    import template_sense

    assert hasattr(template_sense, "__version__")
    assert isinstance(template_sense.__version__, str)
    assert len(template_sense.__version__) > 0
