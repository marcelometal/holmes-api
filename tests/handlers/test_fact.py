#!/usr/bin/python
# -*- coding: utf-8 -*-

from preggy import expect
from tornado.testing import gen_test

from holmes.models import Review
from tests.base import ApiTestCase
from tests.fixtures import DomainFactory, PageFactory, ReviewFactory


class TestFactHandler(ApiTestCase):

    @gen_test
    def test_can_save_fact(self):
        domain = yield DomainFactory.create()
        page = yield PageFactory.create(domain=domain)
        review = yield ReviewFactory.create(page=page)

        url = self.get_url(
            '/page/%s/review/%s/fact' % (
                page.uuid,
                review.uuid
            )
        )

        response = yield self.http_client.fetch(
            url,
            method='POST',
            body='key=test.fact&unit=kb&value=10'
        )

        expect(response.code).to_equal(200)
        expect(response.body).to_equal("OK")

        review = yield Review.objects.get(uuid=review.uuid)

        expect(review).not_to_be_null()
        expect(review.facts).to_length(1)

        fact = review.facts[0]
        expect(fact.key).to_equal('test.fact')
        expect(fact.unit).to_equal('kb')
        expect(fact.value).to_equal('10')