# Copyright (c) 2010 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Top-level presubmit script for kernel.

See http://dev.chromium.org/developers/how-tos/depottools/presubmit-scripts
for more details about the presubmit API built into gcl and git cl.
"""

import subprocess

def CheckPatch(input_api, output_api, source_file_filter=None):
  """Checks that there is a Signed-off-by in the description."""
  output = []
  checkpatch = 'scripts/checkpatch.pl'
  for affected_file in input_api.AffectedSourceFiles(source_file_filter):
    file_name = affected_file.LocalPath()
    if file_name.endswith('.c') or file_name.endswith('.h'):
      cmd = subprocess.Popen([checkpatch, '-f', file_name],
                             stdout=subprocess.PIPE)
      stdout, _ = cmd.communicate()
      if cmd.returncode:
        output.append(output_api.PresubmitPromptWarning(stdout))
  return output

def CheckSignOff(input_api, output_api, source_file_filter=None):
  """Checks that there is a Signed-off-by in the description."""
  output = []
  if input_api.change.DescriptionText().count('Signed-off-by:') == 0:
    output.append(output_api.PresubmitError(
        'This project requires all commits to contain a Signed-off-by:'))
  return output

def CheckChange(input_api, output_api, committing):
    results = []
    results += CheckSignOff(input_api, output_api)
    results += CheckPatch(input_api, output_api)
    return results

def CheckChangeOnUpload(input_api, output_api):
    return CheckChange(input_api, output_api, False)

def CheckChangeOnCommit(input_api, output_api):
    return CheckChange(input_api, output_api, True)
