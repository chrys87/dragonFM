#!/bin/bash
# generate_translations.sh
# Description: A small script to create gettext translation files .pot, .po
#
# Copyright 2019, F123 Consulting, <information@f123.org>
# Copyright 2019, Storm Dragon, <storm_dragon@linux-a11y.org>
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; see the file COPYING.  If not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
#--code--

# Set project name here.
projectName="dragonfm"

if [[ -f "${projectName}.pot" ]]; then
    echo "${projectName}.pot already exists, remove it to regenerate it."
else
    ifs="$IFS"
    IFS=$'\n'
    xgettext -o ${projectName}.pot -d ${projectName} -L python $(find ../src -type f -iname "*.py")
    IFS="$ifs"
fi

if [[ $# -eq 1 ]]; then
    if grep -qw "$1" /etc/locale.gen ; then
        echo "Generating .po file for $1."
        msginit -i "${projectName}.pot" -l $1
        sed -i -e "s/PACKAGE package.$/PACKAGE $projectName./g" \
            -e 's/THE PACKAGE.S COPYRIGHT HOLDER$/F123 Consulting <info@f123.org>/' "${1%.*}.po"
    else
        echo "No locale $1 found, skipping."
    fi
fi

exit 0
