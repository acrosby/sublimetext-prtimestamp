import sublime, sublime_plugin
import datetime
import pprint

TIMEFMT = "%Y-%m-%d %a %H:%M"
year, month, day = 2000, 1, 1
datetime = datetime.datetime(year, month, day)


def duration(line):
    try:
        line = line.split("[")
        t0, t1 = line[1].split("]")[0], line[-1].split("]")[0]
        t0, t1 = datetime.strptime(t0, TIMEFMT), datetime.strptime(t1, TIMEFMT)
        delta = t1 - t0
        delta = (delta.days * 24.) + (delta.seconds / 3600.)
        return delta
    except IndexError:
        return None


class PtstimestampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        now_str = datetime.now().strftime("[%s]" % (TIMEFMT,))
        self.view.insert(edit, self.view.sel()[0].begin(), now_str)


class PtsdurationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for i in range(len(self.view.sel())):
            delta = duration(self.view.substr(self.view.line(self.view.sel()[i])))
            if delta is not None:
                delta = " => %5.2f Hrs" % (delta,)
                self.view.insert(edit, self.view.line(self.view.sel()[i]).end(), delta)


class PtsreportCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        report = {}
        wholedoc = self.view.sel()[0]
        lines = self.view.lines(wholedoc)
        for line in lines:
            line = self.view.substr(line)
            delta = duration(line)
            if delta is not None:
                if "[" in line.split()[0]:
                    project = None
                else:
                    project = line.split()[0]
                report[project] = report.get(project, 0.) + delta
        sublime.set_clipboard(pprint.pformat(report, depth=1, indent=4))


class PtsreportsumCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        report = {}
        wholedoc = self.view.sel()[0]
        lines = self.view.lines(wholedoc)
        for line in lines:
            line = self.view.substr(line)
            delta = duration(line)
            if delta is not None:
                if "[" in line.split()[0]:
                    project = None
                else:
                    project = line.split()[0]
                report[project] = report.get(project, 0.) + delta
        s = 0
        for k in report:
            s += report[k]
        sublime.set_clipboard(str(s))

