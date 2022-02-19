from src.comment import Comment, Author
from src.randomizer import Randomizer
import mock


@mock.patch('random.choice')  # decorator
def test_randomize_with_duplicate_users(mocked_choice):
    comments = [
        Comment(author=Author("John"), text="best friend is Maggie"),
        Comment(Author("Maggie", ""), text="best buddy is John"),
        Comment(Author("John", ""), text="best friend is Maggie not Raj"),
        Comment(Author("Maggie", ""), text="best friend is Maggie"),
        Comment(Author("Persy", ""), text="meow meow meow"),
        Comment(Author("Cat", ""), text="I want food"),
        Comment(Author("Cat", ""), text="I love Persy"),
    ]
    expected_comments_choice = [
        Comment(Author("John", ""), text="best friend is Maggie"),
        Comment(Author("Maggie", ""), text="best buddy is John"),
        Comment(Author("Persy", ""), text="meow meow meow"),
        Comment(Author("Cat", ""), text="I want food"),
    ]

    mocked_choice.return_value = expected_comments_choice[0]
    r = Randomizer(comments, remove_duplicate_users=True)
    assert r.randomize() == expected_comments_choice[0]
    mocked_choice.assert_called_once_with(expected_comments_choice)


@mock.patch('random.choice')  # decorator
def test_randomize_with_no_duplicate_users(mocked_choice):
    comments = [
        Comment(author=Author("John"), text="best friend is Maggie"),
        Comment(Author("Maggie", ""), text="best buddy is John"),
        Comment(Author("John", ""), text="best friend is Maggie not Raj"),
        Comment(Author("Maggie", ""), text="best friend is Maggie"),
        Comment(Author("Persy", ""), text="meow meow meow"),
        Comment(Author("Cat", ""), text="I want food"),
        Comment(Author("Cat", ""), text="I love Persy"),
    ]
    expected_comments = comments

    mocked_choice.return_value = expected_comments[0]
    r = Randomizer(comments, remove_duplicate_users=False)
    assert r.randomize() == expected_comments[0]
    mocked_choice.assert_called_once_with(expected_comments)

@mock.patch('random.choice')  # decorator
def test_randomize_with_duplicate_users_with_text(mocked_choice):
    comments = [
        Comment(author=Author("John"), text="best friend is Maggie"),
        Comment(Author("Maggie", ""), text="best buddy is John"),
        Comment(Author("John", ""), text="best friend is Maggie not Raj"),
        Comment(Author("Maggie", ""), text="best friend is Maggie"),
        Comment(Author("Persy", ""), text="meow meow meow and Cat is not my friend"),
        Comment(Author("Cat", ""), text="I want food"),
        Comment(Author("Cat", ""), text="I love Persy"),
    ]
    expected_comments_choice = [
        Comment(Author("John", ""), text="best friend is Maggie"),
        Comment(Author("Maggie", ""), text="best friend is Maggie"),
        Comment(Author("Persy", ""), text="meow meow meow and Cat is not my friend"),
    ]

    mocked_choice.return_value = expected_comments_choice[0]
    r = Randomizer(comments, remove_duplicate_users=True, specific_text='friend')
    assert r.randomize() == expected_comments_choice[0]
    mocked_choice.assert_called_once_with(expected_comments_choice)
