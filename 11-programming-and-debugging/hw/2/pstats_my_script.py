import pstats
import io


s = io.StringIO()
ps = pstats.Stats("profile.txt", stream=s).sort_stats('tottime')
ps.print_stats()

with open(
        'EpamPython2019/11-programming-and-debugging/hw/2/3_profile_stats.txt', 'w+') as f:
    f.write(s.getvalue())
