#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from uuid import uuid4
from functools import partial

from holmes.cli import BaseCLI
from holmes.models.domain import Domain
from holmes.models.page import Page
from holmes.models.violation import Violation
from holmes.utils import get_domain_from_url


def configure_materials(girl, db, config):
    girl.add_material(
        'domains_details',
        partial(Domain.get_domains_details, db),
        30
    )

    girl.add_material(
        'next_jobs_count',
        partial(Page.get_next_jobs_count, db, config),
        10
    )

    girl.add_material(
        'violation_count_by_category_for_domains',
        partial(Violation.get_group_by_category_id_for_all_domains, db),
        60
    )

    girl.add_material(
        'blacklist_domain_count',
        partial(MaterialConveyor.get_blacklist_domain_count, db),
        600
    )


class MaterialConveyor(object):
    @classmethod
    def get_blacklist_domain_count(cls, db):
        ungrouped = {}
        for urls, count in Violation.get_group_by_value_for_key(db, 'blacklist.domains'):
            for url in urls:
                domain, null = get_domain_from_url(url)
                if domain not in ungrouped:
                    ungrouped[domain] = 0
                ungrouped[domain] += count
        blacklist = sorted(ungrouped.items(), key=lambda xz: -xz[1])
        return [dict(zip(('domain', 'count'), x)) for x in blacklist]


class MaterialWorker(BaseCLI):
    def initialize(self):
        self.uuid = uuid4().hex

        self.error_handlers = [handler(self.config) for handler in self.load_error_handlers()]

        self.connect_sqlalchemy()
        self.connect_to_redis()

        self.configure_material_girl()

    def do_work(self):
        self.info('Running material girl...')
        self.girl.run()


def main():
    worker = MaterialWorker(sys.argv[1:])
    worker.run()

if __name__ == '__main__':
    main()
