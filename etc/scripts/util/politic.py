# -*- coding: utf-8 -*-
# Copyright (c) 2019, Compiler Explorer Authors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import subprocess
import re
import argparse
import sys
from pathlib import Path

date_placeholder = '(<span id="last-changed">).*(</span>)'
date_placeholder_regex = re.compile(date_placeholder)


def update_policy_file(source: Path, dest: Path) -> None:
    policy_last_time = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cd', str(source)]
    ).decode('utf-8').rstrip()

    if len(policy_last_time) == 0:
        print(f'Unable to get git info for {source}')
        sys.exit(1)
    policy_last_commit = subprocess.check_output(['git', 'log', '-1', '--format=%h', str(source)]).decode(
        'utf-8').rstrip()
    print(f'Setting policy {dest} last updated time to {policy_last_time} with commit {policy_last_commit}')
    with source.open('r', encoding='utf-8') as f:
        file_lines = f.readlines()
    with dest.open('w', encoding='utf-8') as f:
        for line in file_lines:
            if re.match(date_placeholder_regex, line):
                f.write(re.sub(date_placeholder_regex,
                               f'\\1Last changed on: <time id="changed-date" datetime="{policy_last_time}">{policy_last_time}</time> <i>(<a href="https://github.com/compiler-explorer/compiler-explorer/commit/{policy_last_commit}" target="_blank">diff</a>)</i>\\2',
                               line))
            else:
                f.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="policy source filename", metavar="SRC", type=Path)
    parser.add_argument("dest", help="policy destination filename", metavar="DEST", type=Path)
    args = parser.parse_args()
    update_policy_file(args.source, args.dest)
