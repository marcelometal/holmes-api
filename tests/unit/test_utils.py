#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

from preggy import expect

from holmes.utils import (
    get_domain_from_url, get_class, load_classes, get_status_code_title
)


class TestUtils(TestCase):

    def test_single_url(self):
        domain, url = get_domain_from_url('http://globo.com')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_null_url(self):
        domain, url = get_domain_from_url(None)
        expect(domain).to_equal('')
        expect(url).to_equal('')

        domain, url = get_domain_from_url('')
        expect(domain).to_equal('')
        expect(url).to_equal('')

    def test_single_https_url(self):
        domain, url = get_domain_from_url('https://globo.com')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('https://globo.com')

    def test_single_url_using_default_scheme(self):
        domain, url = get_domain_from_url('globo.com')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_single_url_using_custom_scheme(self):
        domain, url = get_domain_from_url('globo.com', default_scheme='https')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('https://globo.com')

    def test_single_page_url(self):
        domain, url = get_domain_from_url('http://globo.com/index.html')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_single_page_url_with_port(self):
        domain, url = get_domain_from_url("http://globo.com:80/index.html")
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_page_with_unicode(self):
        domain, url = get_domain_from_url('//globo.com:80/%7Eguido/Python.html')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_page_without_protocol(self):
        domain, url = get_domain_from_url('globo.com/%7Eguido/Python.html')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_page_without_protocol_with_port(self):
        domain, url = get_domain_from_url('globo.com:80/%7Eguido/Python.html')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_page_invalid_protocol(self):
        domain, url = get_domain_from_url('ttp://globo.com')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://globo.com')

    def test_page_with_www(self):
        domain, url = get_domain_from_url('http://www.globo.com:80/%7Eguido/Python.html')
        expect(domain).to_equal('globo.com')
        expect(url).to_equal('http://www.globo.com')

    def test_page_invalid_url(self):
        domain, url = get_domain_from_url('help/Python.html')
        expect(domain).to_equal('')
        expect(url).to_equal('')

    def test_localhost(self):
        domain, url = get_domain_from_url('http://localhost/Python.html')
        expect(domain).to_equal('localhost')
        expect(url).to_equal('http://localhost')

    def test_can_get_class(self):
        from Queue import Queue

        loaded = get_class("Queue.Queue")
        expect(loaded).to_equal(Queue)

    def test_can_get_class_with_more_levels(self):
        from holmes.models.review import Review

        loaded = get_class("holmes.models.review.Review")

        expect(loaded).to_equal(Review)

    def test_can_load_classes(self):
        from holmes.models.domain import Domain
        from holmes.models.page import Page
        from holmes.models.review import Review

        classes = load_classes(default=[
            'holmes.models.domain.Domain',
            'holmes.models.page.Page',
            'holmes.models.review.Review',
        ])

        expect(classes).to_length(3)
        expect(classes[0]).to_equal(Domain)
        expect(classes[1]).to_equal(Page)
        expect(classes[2]).to_equal(Review)

    def test_get_status_code_title(self):
        title = get_status_code_title(500)
        expect(title).to_equal('Internal Server Error')

        title = get_status_code_title(599)
        expect(title).to_equal('Tornado Timeout')

        title = get_status_code_title(120)
        expect(title).to_equal('Unknown')
