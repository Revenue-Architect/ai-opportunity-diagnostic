"""Package one completed diagnostic for internal email delivery."""

import argparse
import os
from pathlib import Path
import re
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


def package(output, entries):
    output = output.resolve()
    if output.suffix.lower() != '.zip':
        raise ValueError('Output must have a .zip extension')
    for member, source in entries:
        if not source.is_file():
            raise ValueError(f'Missing file for {member}: {source}')
        if source.resolve() == output:
            raise ValueError(f'Output cannot also be an input: {source}')

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix='.diagnostic-', suffix='.zip', delete=False) as temporary:
        staged = Path(temporary.name)
    try:
        with ZipFile(staged, 'w', compression=ZIP_DEFLATED) as archive:
            for member, source in entries:
                archive.write(source, member)
        with ZipFile(staged) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP integrity check failed')
        os.replace(staged, output)
    finally:
        staged.unlink(missing_ok=True)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--owner-report', required=True, type=Path)
    parser.add_argument('--build-brief', required=True, type=Path)
    parser.add_argument('--input', type=Path, help='Scoring input JSON')
    parser.add_argument('--scorer-output', type=Path, help='Unedited scorer output')
    parser.add_argument('--source-file', action='append', default=[], type=Path, help='Raw source file used in this diagnostic. Repeat as needed.')
    args = parser.parse_args()

    entries = [('owner-report.md', args.owner_report), ('build-brief.md', args.build_brief)]
    if args.input:
        entries.append(('raw/diagnostic-input.json', args.input))
    if args.scorer_output:
        entries.append(('raw/scorer-output.md', args.scorer_output))
    for number, source in enumerate(args.source_file, 1):
        filename = re.sub(r'[^a-zA-Z0-9._-]+', '_', source.name)
        entries.append((f'raw/sources/{number:02d}-{filename}', source))

    try:
        output = package(args.output, entries)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Could not package diagnostic: {error}\n')
    print(output)


if __name__ == '__main__':
    main()
