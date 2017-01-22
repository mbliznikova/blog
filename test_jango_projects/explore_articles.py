from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from __builtin__ import classmethod
import datetime
import os
import lorem_ipsum


def uniform_text(s):
    return ' '.join(s.split())


class ArticlesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.suffix = os.urandom(4).encode('hex')

        self.driver.get("http://127.0.0.1:" +
                        os.environ.get('TEST_PORT', '8000') + "/articles/")

    def _check_footer_and_header(self):
        self.assertTrue(self.is_element_present(By.CLASS_NAME, 'footer'))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, 'Blog Articles'))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, 'New Article'))
        link_new = self.driver.find_element_by_link_text('New Article')
        self.assertTrue(
            link_new.get_attribute('href').endswith('/articles/new_article/'))
        link_blog = self.driver.find_element_by_link_text('Blog Articles')
        self.assertTrue(
            link_blog.get_attribute('href').endswith('/articles/'))

    def _write_comment(self, author_name, comment_text):
        author_fied = self.driver.find_element_by_name('author')
        author_fied.clear()
        author_fied.send_keys(author_name)
        comment_field = self.driver.find_element_by_name('comment_text')
        comment_field.clear()
        comment_field.send_keys(comment_text)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def _write_new_article(self, author_name, article_title, article_content):
        author_fied = self.driver.find_element_by_name('author')
        author_fied.clear()
        author_fied.send_keys(author_name)
        title_field = self.driver.find_element_by_name('article_header')
        title_field.clear()
        title_field.send_keys(article_title)
        text_field = self.driver.find_element_by_name('article_text')
        text_field.clear()
        text_field.send_keys(article_content)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def _check_requires_not_empty(self):
        not_filled = self.driver.find_element_by_css_selector(
            'div.form-group.has-error span.help-block')
        self.assertEqual('This field is required.', not_filled.text)

    def test_jumbotron_exists(self):
        self._check_footer_and_header()
        self.assertTrue(self.is_element_present(By.CLASS_NAME, 'jumbotron'))
        self.assertTrue(self.is_element_present(
            By.XPATH, "//*[contains(text(), \"Margarita's Blog\")]"))
        element = self.driver.find_element_by_css_selector('div.jumbotron p')
        self.assertEqual('This project was developed primarily for learning '
                         'Django, Python and Selenium. Nothing to see here, '
                         'move along!', element.text)

    def test_find_and_read_article(self):
        self.driver.find_element_by_link_text('New Article').click()
        self._check_footer_and_header()
        self._write_new_article('John Doe',
                                'Lorem Ipsum {0}'.format(self.suffix),
                                lorem_ipsum.THREE_PARAGRAPHS)
        self.driver.find_element_by_link_text('Blog Articles').click()

        # Find More button for created article and click it
        self.driver.find_element_by_xpath(
            '//h2[contains(text(), "{0}")]/'
            '..//a[contains(text(), "More")]'.format(self.suffix)).click()

        self._check_footer_and_header()
        title_elem = self.driver.find_element_by_class_name(
            'blog-post-title')
        self.assertEqual('Lorem Ipsum {0}'.format(self.suffix),
                         title_elem.text)
        article_meta = self.driver.find_element_by_class_name(
            'blog-post-meta')
        self.assertIn('John Doe', article_meta.text)
        # TODO: check that current date/time is in article_meta.text
        article_text = self.driver.find_elements_by_css_selector(
            'div.blog-post > p:not([class])')
        self.assertEqual(3, len(article_text))
        paragraphs = lorem_ipsum.THREE_PARAGRAPHS.split('\n\n')
        for i in range(3):
            self.assertEqual(uniform_text(paragraphs[i]),
                             uniform_text(article_text[i].text))

    def test_create_valid_article(self):
        self.driver.find_element_by_link_text('New Article').click()
        self._check_footer_and_header()
        self._write_new_article('John Doe',
                                'Lorem Ipsum {0}'.format(self.suffix),
                                lorem_ipsum.THREE_PARAGRAPHS)
        self._check_footer_and_header()
        title_elem = self.driver.find_element_by_class_name(
            'blog-post-title')
        self.assertEqual('Lorem Ipsum {0}'.format(self.suffix),
                         title_elem.text)
        article_meta = self.driver.find_element_by_class_name(
            'blog-post-meta')
        self.assertIn('John Doe', article_meta.text)
        # TODO: check that current date/time is in article_meta.text
        article_text = self.driver.find_elements_by_css_selector(
            'div.blog-post > p:not([class])')
        self.assertEqual(3, len(article_text))
        paragraphs = lorem_ipsum.THREE_PARAGRAPHS.split('\n\n')
        for i in range(3):
            self.assertEqual(uniform_text(paragraphs[i]),
                             uniform_text(article_text[i].text))

    def test_create_invalid_article(self):
        self.driver.find_element_by_link_text('New Article').click()
        default_header = self.driver.find_element_by_name(
            'article_header').get_attribute('value')
        self.assertEqual('No subject', default_header)
        self._write_new_article('John Doe',
                                'Lorem Ipsum {0}'.format(self.suffix), '')
        self._check_footer_and_header()
        self._check_requires_not_empty()
        self._write_new_article('John Doe', '',
                                lorem_ipsum.THREE_PARAGRAPHS)
        self._check_footer_and_header()
        self._check_requires_not_empty()
        self._write_new_article('', 'Lorem Ipsum {0}'.format(self.suffix),
                                lorem_ipsum.THREE_PARAGRAPHS)
        self._check_footer_and_header()
        self._check_requires_not_empty()

    def test_create_article_with_duplicated_header(self):
        self.driver.find_element_by_link_text('New Article').click()
        header_to_duplicate = 'Lorem Ipsum {0}'.format(self.suffix)
        self._write_new_article('John Doe', header_to_duplicate,
                                lorem_ipsum.THREE_PARAGRAPHS)
        self._check_footer_and_header()
        self.driver.find_element_by_link_text('New Article').click()
        self._write_new_article('John Doe', header_to_duplicate,
                                lorem_ipsum.THREE_PARAGRAPHS)
        self._check_footer_and_header()
        not_duplicate = self.driver.find_element_by_css_selector(
            'div.form-group.has-error span.help-block')
        self.assertEqual('Article with this Article header already exists.',
                         not_duplicate.text)

    def test_write_valid_comment(self):
        self.driver.find_element_by_link_text('New Article').click()
        self._check_footer_and_header()
        self._write_new_article('John Doe',
                                'Lorem Ipsum {0}'.format(self.suffix),
                                lorem_ipsum.THREE_PARAGRAPHS)
        self.driver.find_element_by_link_text('Blog Articles').click()

        # Find More button for created article and click it
        self.driver.find_element_by_xpath(
            '//h2[contains(text(), "{0}")]/'
            '..//a[contains(text(), "More")]'.format(self.suffix)).click()
        self._check_footer_and_header()
        self._write_comment('John Bull', 'So nice!')
        self._check_footer_and_header()
        comment_meta = self.driver.find_element_by_class_name(
            'blog-post-comment-meta')
        self.assertIn('John Bull', comment_meta.text)
        self.assertTrue(self.is_element_present(
            By.XPATH, "//*[contains(text(), 'So nice!')]"))

    def test_write_invalid_comment(self):
        self.driver.find_element_by_link_text('New Article').click()
        self._check_footer_and_header()
        self._write_new_article('John Doe',
                                'Lorem Ipsum {0}'.format(self.suffix),
                                lorem_ipsum.THREE_PARAGRAPHS)
        self.driver.find_element_by_link_text('Blog Articles').click()

        # Find More button for created article and click it
        self.driver.find_element_by_xpath(
            '//h2[contains(text(), "{0}")]/'
            '..//a[contains(text(), "More")]'.format(self.suffix)).click()
        self._check_footer_and_header()
        self._write_comment('', 'So nice!')
        self._check_footer_and_header()
        self._check_requires_not_empty()
        self._write_comment('John Bull', '')
        self._check_footer_and_header()
        self._check_requires_not_empty()

    def is_element_present(self, how, what):
        """
        Utility method to check presence of an element on page
        :params how: By locator type
        :params what: locator value
        """
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True


if __name__ == '__main__':
    unittest.main()
