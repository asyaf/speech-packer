import mock
import pytest
import random

from speech_packer import Packer, SpeechAnalyzer

ITEMS = ['t-shirt', 'jeans', 'raincoat', 'sneakers', 'hiking boots']

@mock.patch("speech_packer.SpeechAnalyzer")
def test__add_item(mock_analyzer):
    item = random.choice(ITEMS)
    mock_analyzer.process_single_phrase.return_value = item
    pckr = Packer(mock_analyzer)
    pckr._add_item()
    assert pckr._to_pack == set([item])

@mock.patch("speech_packer.SpeechAnalyzer")
def test__pack_item(mock_analyzer):
    item = random.choice(ITEMS)
    mock_analyzer.process_single_phrase.return_value = item
    pckr = Packer(mock_analyzer)
    pckr._add_item()
    pckr._pack_item()
    assert pckr._to_pack == set()
    assert pckr._packed == set([item])

@mock.patch("speech_packer.SpeechAnalyzer")
def test__pack_item_failure(mock_analyzer):
    item = random.choice(ITEMS)
    mock_analyzer.process_single_phrase.return_value = item
    pckr = Packer(mock_analyzer)
    pckr._pack_item()
    assert pckr._to_pack == set()
    assert pckr._packed == set()

@mock.patch("speech_packer.SpeechAnalyzer")
def test__delete_item(mock_analyzer):
    item1 = ITEMS[0]
    item2 = ITEMS[1]
    item3 = ITEMS[2]
    mock_analyzer.process_single_phrase.return_value = item1
    pckr = Packer(mock_analyzer)
    pckr._add_item()
    mock_analyzer.process_single_phrase.return_value = item2

    pckr._add_item()
    assert pckr._to_pack == set([item1, item2])
    pckr._pack_item()
    assert pckr._to_pack == set([item1])
    assert pckr._packed == set([item2])

    # deleting a non existent item
    mock_analyzer.process_single_phrase.return_value = item3
    pckr._delete_item()
    assert pckr._to_pack == set([item1])
    assert pckr._packed == set([item2])

    # deleting an item that was packed
    mock_analyzer.process_single_phrase.return_value = item2
    pckr._delete_item()
    assert pckr._to_pack == set([item1])
    assert pckr._packed == set()

    # deleting an item that was added
    mock_analyzer.process_single_phrase.return_value = item1
    pckr._delete_item()
    assert pckr._to_pack == set()
    assert pckr._packed == set()


