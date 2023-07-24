import os
import sys
from typing import Dict

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from _python_core.translations import merge


def translate(msg: str, lang: str = "en") -> str:
    lang = "en" if lang not in sentences.keys() else lang
    return sentences[lang].get(msg, msg)


sentences = {
    "en": {
        "COMMON_DATA": "Common data.",
        "ONLY_ENGLISH": "Only English.",
    },
    "es": {
        "COMMON_DATA": "Datos comunes.",
        "ONLY_SPANISH": "Solo español.",
    },
}


class TestTranslations:
    def test_translate_existing(self) -> None:
        assert translate("COMMON_DATA") == "Common data."

    def test_translate_existing_en_es(self) -> None:
        assert translate("COMMON_DATA", "es") == "Datos comunes."

    def test_translate_only_existing_en(self) -> None:
        assert translate("ONLY_ENGLISH") == "Only English."

    def test_translate_only_existing_en_2(self) -> None:
        assert translate("ONLY_ENGLISH", "en") == "Only English."

    def test_translate_only_existing_es(self) -> None:
        assert translate("ONLY_SPANISH") == "ONLY_SPANISH"

    def test_translate_wrong_language(self) -> None:
        assert translate("ONLY_SPANISH", "fr") == "ONLY_SPANISH"


class TestTranslationsMerge:
    def test_merge(self) -> None:  # sourcery skip: class-extract-method
        commonDict: Dict = {"en": {"1": "one"}, "es": {"1": "uno"}}
        serviceDict: Dict = {"en": {"2": "two"}, "es": {"2": "dos"}}

        newTranslations = merge(commonDict, serviceDict)
        assert newTranslations["en"].get("1") == "one"
        assert newTranslations["es"].get("1") == "uno"
        assert newTranslations["en"].get("2") == "two"
        assert newTranslations["es"].get("2") == "dos"

    def test_merge_new_lang(self) -> None:
        commonDict: Dict = {"en": {"1": "one"}, "es": {"1": "uno"}}
        serviceDict: Dict = {"fr": {"1": "une", "2": "deux"}}

        newTranslations = merge(commonDict, serviceDict)
        assert newTranslations["en"].get("1") == "one"
        assert newTranslations["es"].get("1") == "uno"
        assert newTranslations["fr"].get("1") == "une"
        assert newTranslations["en"].get("2") is None
        assert newTranslations["es"].get("2") is None
        assert newTranslations["fr"].get("2") == "deux"

    def test_merge_new_lang_2(self) -> None:
        commonDict: Dict = {}
        serviceDict: Dict = {"fr": {"1": "une", "2": "deux"}}

        newTranslations = merge(commonDict, serviceDict)
        assert newTranslations["fr"].get("1") == "une"
        assert newTranslations["fr"].get("2") == "deux"

    def test_merge_new_lang_3(self) -> None:
        commonDict: Dict = {"en": {"1": "one"}, "es": {"1": "uno"}}
        serviceDict: Dict = {}

        newTranslations = merge(commonDict, serviceDict)
        assert newTranslations["en"].get("1") == "one"
        assert newTranslations["es"].get("1") == "uno"
        assert newTranslations["en"].get("2") is None
        assert newTranslations["es"].get("2") is None
