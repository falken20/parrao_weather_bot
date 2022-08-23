import config_fk


def test_config_vars():
    assert config_fk.__title__ == "Cercedilla Weather Twitter Bot"
    assert config_fk.__version__ == "1.2.0"
    assert config_fk.__author__ == "Richi Rod"
    assert config_fk.__url_github__ == "https://github.com/falken20/"
    assert config_fk.__url_twitter__ == "https://twitter.com/richionline"
    assert config_fk.__url_linkedin__ == "https://www.linkedin.com/in/richionline/"
    assert config_fk.__license__ == "MIT License"
    assert config_fk.__copyright__ == "© 2020 by Richi Rod AKA @richionline / falken20"
