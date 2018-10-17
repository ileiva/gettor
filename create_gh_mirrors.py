# -*- coding: utf-8 -*-
#
# This file is part of GetTor
#
# :authors: Israel Leiva <ilv@torproject.org>
#           see also AUTHORS file
#
# :license: This is Free Software. See LICENSE for license information.

"""create_gh_mirrors -- Create landing page and readme for Github."""

import os
import configparser

import github3

import gettor.core


def create_readme(tpl_path, md_path, tb_version, links):
    """Create README file with links stored in github.links.

    :param: tpl_path (string) path to file used as template.
    :param: md_path (string) path to file generated.
    :param: tb_version (string) tor browser version.
    :param: links (object) github links.

    """
    lcs = ['FA', 'ZH', 'TR', 'EN']

    md_file = open(md_path, 'w')
    with open(tpl_path, 'r') as tpl_file:
        content_md = tpl_file.read()

        for lc in lcs:
            win_link = links.get('windows', lc.lower())
            win_pkg, win_sig, win_sha = [e for e in win_link.split("$") if e]

            osx_link = links.get('osx', lc.lower())
            osx_pkg, osx_sig, osx_sha = [e for e in osx_link.split("$") if e]

            linux_links = links.get('linux', lc.lower())
            linux32_link, linux64_link = linux_links.split(',')
            linux32_pkg, linux32_sig, linux32_sha = [
                e for e in linux32_link.split("$") if e
            ]
            linux64_pkg, linux64_sig, linux64_sha = [
                e for e in linux64_link.split("$") if e
            ]

            content_md = content_md.replace(
                "%WINDOWS_{}%".format(lc), win_pkg
            )
            content_md = content_md.replace(
                "%WINDOWS_{}_SIG%".format(lc), win_sig
            )

            content_md = content_md.replace(
                "%OSX_{}%".format(lc), osx_pkg
            )
            content_md = content_md.replace(
                "%OSX_{}_SIG%".format(lc), osx_sig
            )

            content_md = content_md.replace(
                "%LINUX32_{}%".format(lc), linux32_pkg
            )
            content_md = content_md.replace(
                "%LINUX32_{}_SIG%".format(lc), linux32_sig
            )
            content_md = content_md.replace(
                "%LINUX64_{}%".format(lc), linux64_pkg
            )
            content_md = content_md.replace(
                "%LINUX64_{}_SIG%".format(lc), linux64_sig
            )

        content_md = content_md.replace("%TB_VERSION%", tb_version)
        md_file.write(content_md)

    print(("README generated with Tor Browser %s" % tb_version))


def create_landing_html(tpl_path, html_path, tb_version, links):
    """Create README file with links stored in github.links.

    :param: tpl_path (string) path to file used as template.
    :param: html_path (string) path to file generated.
    :param: tb_version (string) tor browser version.
    :param: links (object) github links.

    """
    lcs = ['FA', 'ZH', 'TR', 'EN']

    html_file = open(html_path, 'w')
    with open(tpl_path, 'r') as tpl_file:
        content_html = tpl_file.read().replace('\n', '')

        for lc in lcs:
            win_link = links.get('windows', lc.lower())
            win_pkg, win_sig, win_sha = [e for e in win_link.split("$") if e]

            osx_link = links.get('osx', lc.lower())
            osx_pkg, osx_sig, osx_sha = [e for e in osx_link.split("$") if e]

            linux_links = links.get('linux', lc.lower())
            linux32_link, linux64_link = linux_links.split(',')
            linux32_pkg, linux32_sig, linux32_sha = [
                e for e in linux32_link.split("$") if e
            ]
            linux64_pkg, linux64_sig, linux64_sha = [
                e for e in linux64_link.split("$") if e
            ]

            content_html = content_html.replace(
                "%WINDOWS_{}%".format(lc), win_pkg
            )
            """
            content_html = content_html.replace(
                "%WINDOWS_{}_SIG%".format(lc), win_sig
            )
            """
            content_html = content_html.replace(
                "%OSX_{}%".format(lc), osx_pkg
            )
            """
            content_html = content_html.replace(
                "%OSX_{}_SIG%".format(lc), osx_sig
            )
            """
            content_html = content_html.replace(
                "%LINUX32_{}%".format(lc), linux32_pkg
            )
            """
            content_html = content_html.replace(
                "%LINUX32_{}_SIG%".format(lc), linux32_sig
            )
            """
            content_html = content_html.replace(
                "%LINUX64_{}%".format(lc), linux64_pkg
            )
            """
            content_html = content_html.replace(
                "%LINUX64_{}_SIG%".format(lc), linux64_sig
            )
            """

        content_html = content_html.replace(
            "%TB_VERSION%", tb_version
        )
        html_file.write(content_html)

    print(("HTML generated with Tor Browser %s" % tb_version))


def main():
    """Generate HTML and md files and update it in Github."""
    github_links = 'providers/github.links'
    tb_version_path = 'latest_torbrowser.cfg'
    md_path = 'upload/readme_gh.md'
    html_path = 'upload/landing_gh.html'
    md_tpl_path = 'upload/readme_gh.tpl'
    html_tpl_path = 'upload/landing_gh.tpl'
    github_access_token = ''

    try:
        tb_version_config = configparser.ConfigParser()
        tb_version_config.read(tb_version_path)
        tb_version = tb_version_config['version']['current']

    except:
        raise SystemExit("Failed to parse %s. Does it exist?" % tb_version_path)
        # TODO add some hint how to generate it

    links = configparser.ConfigParser()
    links.read(github_links)

    create_landing_html(html_tpl_path, html_path, tb_version, links)
    create_readme(md_tpl_path, md_path, tb_version, links)

    landing = open(html_path, 'r')
    content_landing = landing.read().replace('\n', '')

    readme = open(md_path, 'r')
    content_readme = readme.read()

    gh = github3.login(token=github_access_token)
    repo_landing = gh.repository('thetorproject', 'gettor')
    repo_readme = gh.repository('thetorproject', 'gettorbrowser')

    file_landing_gh = repo_landing.file_contents('index.html', 'gh-pages')
    file_readme_gh = repo_readme.file_contents('README.md')

    data_landing = {
        'message': 'Updating landing page.',
        'content': content_landing,
        'branch': 'gh-pages'
    }

    data_readme = {
        'message': 'Updating README.',
        'content': content_readme
    }

    file_landing_gh.update(**data_landing)
    print ("Landing page updated in gettor")

    file_readme_gh.update(**data_readme)
    print ("README updated in gettorbrowser")

if __name__ == "__main__":
    main()
