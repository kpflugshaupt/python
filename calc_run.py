import re
import sys
import appex
import clipboard
import console
import webbrowser


# Find text to analyse

phases     = ''
draft_uuid = ''

if appex.is_running_extension():
  # 1. running as extension?
  phases = str(appex.get_text())
else:
  # 2. started with arguments?
  if len(sys.argv) > 1:
    draft = re.match('draft:(.*)', sys.argv[1])
    if draft:
      draft_uuid = draft.group(1)
      phases = ' '.join(sys.argv[2:])
    else:
      phases = ' '.join(sys.argv[1:])
  
# 3. text on clipboard?
if phases == '':
  phases = clipboard.get()

# 4. default sample text
if phases == '':
  phases = console.input_alert('Enter phases', '',
    '5 min z1, 35min z2, 15 min z3', hide_cancel_button=True)


# Set up variables

# avg pace for each zone
avgPace = [5.37, 4.80, 4.07, 3.80, 3.25]

time      = 0
totalTime = 0
dist      = 0
totalDist = 0
cnt       = 1


# Subroutines
def rd(num: float) -> float:
  return round(num, 1)

def test_rd:
  assert rd(3.0) == 3.0
  assert rd(3.14) == 3.1
  assert rd(3.15) == 3.2
  assert rd(-1.15) == -1.2


def avg_pace(zone: int) -> float:
  return avgPace[zone-1]


# Split and parse
phaseSep = ' *[,\n] *'
output = 'INPUT: ' + phases

distPattern = re.compile(' *([\.\d]*) *[kK]m *[Zz](\d)')
milePattern = re.compile(' *([\.\d]*) *[mM]i *[Zz](\d)')
timePattern = re.compile(' *([\.\d]*) *[mM]in *[Zz](\d)')

for phase in re.split(phaseSep, phases):
  # Test for patterns
  m_dist = distPattern.match(phase)
  m_mile = milePattern.match(phase)
  m_time = timePattern.match(phase)
  if m_dist:
    dist = float(m_dist.group(1))
    zone = int(m_dist.group(2))
    time = dist * avg_pace(zone)
    output += '\n{}. Z{}: {} min, {} km'.format(cnt, zone, rd(time), dist)
  elif m_mile:
    dist = 1.61 * float(m_mile.group(1))
    zone = int(m_mile.group(2))
    time = dist * avg_pace(zone)
    output += '\n{}. Z{}: {} min, {} km'.format(cnt, zone, rd(time), dist)
  elif m_time:
    time = float(m_time.group(1))
    zone = int(m_time.group(2))
    dist = time / avg_pace(zone)
    output += '\n{}. Z{}: {} min, {} km'.format(cnt, zone, time, rd(dist))
  else:
    output += '\nno match'
    time = 0
    dist = 0
        
  # sum up time and distance
  totalTime += time
  totalDist += dist
  cnt       += 1

if totalDist > 0:
  totalPace = totalTime/totalDist
else:
  totalPace = 0
  
output += '\nTOTAL: {} min, {} km, {} min/km'.format(rd(totalTime), rd(totalDist), rd(totalPace))


# Show output, finish
console.alert('RUN', output, 'OK', hide_cancel_button=True)

# Return to "drafts", if that's where we came from
if draft_uuid != '':
  webbrowser.open('drafts4://x-callback-url/open?uuid='+draft_uuid)
