from yt_comment_picker.comment import Comment, Author
from yt_comment_picker.randomizer import Randomizer
import mock


@mock.patch('random.choice')  # decorator
def test_randomize_with_duplicate_users(mocked_choice):
    comments = [
        Comment(Author("John", link="link_john"), text="best friend is Maggie"),
        Comment(Author("Maggie", link="link_maggie"), text="best buddy is John"),
        Comment(Author("John", link="link_john"), text="best friend is Maggie not Raj"),
        Comment(Author("John", link="link_decoy_john"), text="best friend is Raj"),
        Comment(Author("Maggie", link="link_maggie"), text="best friend is Maggie"),
        Comment(Author("Persy", link="link_persy"), text="meow meow meow"),
        Comment(Author("Cat", link="link_cat"), text="I want food"),
        Comment(Author("Cat", link="link_cat"), text="I love Persy"),
    ]
    expected_comments_choice = [
        Comment(Author("John", link="link_john"), text="best friend is Maggie"),
        Comment(Author("Maggie", link="link_maggie"), text="best buddy is John"),
        Comment(Author("John", link="link_decoy_john"), text="best friend is Raj"),
        Comment(Author("Persy", link="link_persy"), text="meow meow meow"),
        Comment(Author("Cat", link="link_cat"), text="I want food"),
    ]

    mocked_choice.return_value = expected_comments_choice[0]
    r = Randomizer(comments, remove_duplicate_users=True)
    assert r.randomize() == expected_comments_choice[0]
    mocked_choice.assert_called_once_with(expected_comments_choice)


@mock.patch('random.choice')  # decorator
def test_randomize_with_no_duplicate_users(mocked_choice):
    comments = [
        Comment(Author("John", link="link_john"), text="best friend is Maggie"),
        Comment(Author("Maggie", link="link_maggie"), text="best buddy is John"),
        Comment(Author("John", link="link_john"), text="best friend is Maggie not Raj"),
        Comment(Author("John", link="link_decoy_john"), text="best friend is Raj"),
        Comment(Author("Maggie", link="link_maggie"), text="best friend is Maggie"),
        Comment(Author("Persy", link="link_persy"), text="meow meow meow"),
        Comment(Author("Cat", link="link_cat"), text="I want food"),
        Comment(Author("Cat", link="link_cat"), text="I love Persy"),
    ]
    expected_comments = comments

    mocked_choice.return_value = expected_comments[0]
    r = Randomizer(comments, remove_duplicate_users=False)
    assert r.randomize() == expected_comments[0]
    mocked_choice.assert_called_once_with(expected_comments)

@mock.patch('random.choice')  # decorator
def test_randomize_with_duplicate_users_with_text(mocked_choice):
    comments = [
        Comment(Author("John", link="link_john"), text="best friend is Maggie"),
        Comment(Author("Maggie", link="link_maggie"), text="best buddy is John"),
        Comment(Author("John", link="link_john"), text="best friend is Maggie not Raj"),
        Comment(Author("John", link="link_decoy_john"), text="best friend is Raj"),
        Comment(Author("Maggie", link="link_maggie"), text="best friend is Maggie"),
        Comment(Author("Persy", link="link_persy"), text="meow and Cat is not my friend"),
        Comment(Author("Cat", link="link_cat"), text="I want food"),
        Comment(Author("Cat", link="link_cat"), text="I love Persy"),
    ]
    expected_comments_choice = [
        Comment(Author("John", link="link_john"), text="best friend is Maggie"),
        Comment(Author("John", link="link_decoy_john"), text="best friend is Raj"),
        Comment(Author("Maggie", link="link_maggie"), text="best friend is Maggie"),
        Comment(Author("Persy", link="link_persy"), text="meow and Cat is not my friend"),
    ]

    mocked_choice.return_value = expected_comments_choice[0]
    r = Randomizer(comments, remove_duplicate_users=True, specific_text='friend')
    assert r.randomize() == expected_comments_choice[0]
    mocked_choice.assert_called_once_with(expected_comments_choice)
