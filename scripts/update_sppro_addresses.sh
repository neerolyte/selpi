#!/bin/bash

main() {
	set -euo pipefail

	settings_template_file="${1:-}"
	if [[ -z "$settings_template_file" ]]; then
		echo "ERROR: the path to the DefaultSettingsTemplate.cs file must be supplied on the first line"
		exit 1
	fi

	write_sppro_addresses
}

write_sppro_addresses() {
	get_full_file_contents > "$(dirname "$0")/../memory/sppro_addresses.py"
}

get_full_file_contents() {
	echo "ADDRESSES = {"
		get_address_lines
	echo "}"
}

get_address_lines() {
	get_const_lines | sed -r 's/^    internal const uint Add(.*) = (.*);/    "\1": \2,/g'
}

get_const_lines() {
	grep 'internal const uint Add' "$settings_template_file"
}

main "$@"
