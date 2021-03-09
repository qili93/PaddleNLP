# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import json
import os

from paddle.dataset.common import md5file
from paddle.utils.download import get_path_from_url
from paddlenlp.utils.env import DATA_HOME
from . import DatasetBuilder

__all__ = ['LCQMC']


class LCQMC(DatasetBuilder):
    """
    LCQMC:A Large-scale Chinese Question Matching Corpus
    More information please refer to `https://www.aclweb.org/anthology/C18-1166/`

    """

    URL = "https://bj.bcebos.com/paddlehub-dataset/lcqmc.tar.gz"
    MD5 = "62a7ba36f786a82ae59bbde0b0a9af0c"
    META_INFO = collections.namedtuple('META_INFO', ('file', 'md5'))
    SPLITS = {
        'train': META_INFO(
            os.path.join('lcqmc', 'train.tsv'),
            '2193c022439b038ac12c0ae918b211a1'),
        'dev': META_INFO(
            os.path.join('lcqmc', 'dev.tsv'),
            'c5dcba253cb4105d914964fd8b3c0e94'),
        'test': META_INFO(
            os.path.join('lcqmc', 'test.tsv'),
            '8f4b71e15e67696cc9e112a459ec42bd'),
    }

    def _get_data(self, mode, **kwargs):
        default_root = DATA_HOME
        filename, data_hash = self.SPLITS[mode]
        fullname = os.path.join(default_root, filename)
        if not os.path.exists(fullname) or (data_hash and
                                            not md5file(fullname) == data_hash):
            fullname = os.path.join(default_root, filename)

        return fullname

    def _read(self, filename):
        """Reads data."""
        with open(filename, 'r', encoding='utf-8') as f:
            head = None
            for line in f:
                data = line.strip().split("\t")
                if not head:
                    head = data
                else:
                    query, title, label = data
                    yield {"query": query, "title": title, "label": label}

    def get_labels(self):
        """
        Return labels of the LCQMC object.
        """
        return ["0", "1"]
