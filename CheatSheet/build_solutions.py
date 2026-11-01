#!/usr/bin/env python3
"""Builds past_exam_solutions.html (render to PDF with render_pdf.js).

Each answer is written once in A[...] and reused wherever the professor
repeated the question, so repeated questions always get identical answers.
"""
import html
import textwrap

def code(s):
    body = textwrap.dedent(s).strip("\n")
    cls = ' class="long"' if body.count("\n") >= 16 else ""   # long blocks go 2-column in compact mode
    return f"<pre{cls}>" + html.escape(body) + "</pre>"

def gantt(segs, total):
    cells, ticks = [], []
    for label, a, b, cls in segs:
        w = (b - a) / total * 100
        cells.append(f'<div class="{cls}" style="width:{w:.3f}%">{label}</div>')
        ticks.append(f'<span style="width:{w:.3f}%">{a}</span>')
    ticks[-1] = ticks[-1].replace("</span>", f'<b style="float:right">{segs[-1][2]}</b></span>')
    return f'<div class="gantt">{"".join(cells)}</div><div class="ticks">{"".join(ticks)}</div>'

# ----------------------------------------------------------------- diagrams
SVG_DEFS = """<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker></defs>"""

FORK_TREE = f"""<svg viewBox="0 0 420 215" width="400" class="fig" font-size="11" font-family="Arial">{SVG_DEFS}
<g stroke="#222" fill="none">
<line x1="200" y1="30" x2="110" y2="80"/><line x1="200" y1="30" x2="300" y2="80"/>
<line x1="110" y1="80" x2="55" y2="135"/><line x1="110" y1="80" x2="165" y2="135"/>
<line x1="55" y1="135" x2="55" y2="185"/></g>
<g font-size="10" fill="#0b4f8a"><text x="125" y="50">fork ①</text><text x="255" y="50">fork ③</text>
<text x="40" y="108">fork ②</text><text x="140" y="108">fork ③</text><text x="60" y="165">fork ③</text></g>
<g fill="#fff" stroke="#222"><circle cx="200" cy="25" r="15"/><circle cx="110" cy="80" r="15" fill="#ffe7b0"/><circle cx="300" cy="80" r="15"/>
<circle cx="55" cy="135" r="15" fill="#ffe7b0"/><circle cx="165" cy="135" r="15"/><circle cx="55" cy="190" r="15"/></g>
<g text-anchor="middle"><text x="200" y="29">P0</text><text x="110" y="84">C1</text><text x="300" y="84">C3</text>
<text x="55" y="139">C2</text><text x="165" y="139">C4</text><text x="55" y="194">C5</text></g>
<g font-size="10"><text x="128" y="78">+1 thread</text><text x="73" y="133">+1 thread</text></g>
<text x="235" y="160" font-size="10">shaded = runs thread_create()</text>
<text x="235" y="175" font-size="10">6 processes, 2 created threads</text></svg>"""

MLFQ_5 = f"""<svg viewBox="0 0 600 250" width="560" class="fig" font-size="11" font-family="Arial">{SVG_DEFS}
<g stroke="#222" fill="#eef3fa">
<rect x="170" y="15"  width="250" height="28"/><rect x="170" y="60"  width="250" height="28"/>
<rect x="170" y="105" width="250" height="28"/><rect x="170" y="150" width="250" height="28"/>
<rect x="170" y="195" width="250" height="28"/></g>
<g text-anchor="middle"><text x="295" y="33">Q0 system process (fixed, priority/FCFS)</text>
<text x="295" y="78">Q1 faculty interactive  (RR q = 8 ms)</text><text x="295" y="123">Q2 student interactive (RR q = 8 ms)</text>
<text x="295" y="168">Q3 faculty batch  (RR q = 16 ms)</text><text x="295" y="213">Q4 student batch  (FCFS)</text></g>
<g stroke="#a40000" fill="none" marker-end="url(#ar)">
<path d="M420,74 H450 V164 H422"/><path d="M420,119 H480 V209 H422"/></g>
<g stroke="#0a6b2d" fill="none" marker-end="url(#ar)">
<path d="M170,164 H140 V74 H168"/><path d="M170,209 H110 V119 H168"/></g>
<g stroke="#222" fill="none" marker-end="url(#ar)"><path d="M20,68 H168"/><path d="M20,113 H168"/></g>
<text x="2" y="60" font-size="10">new faculty</text><text x="2" y="105" font-size="10">new student</text>
<text x="486" y="140" font-size="10" fill="#a40000">used whole</text><text x="486" y="153" font-size="10" fill="#a40000">quantum →</text><text x="486" y="166" font-size="10" fill="#a40000">demote</text>
<text x="2" y="160" font-size="10" fill="#0a6b2d">blocked for I/O</text><text x="2" y="173" font-size="10" fill="#0a6b2d">early / aging</text><text x="2" y="186" font-size="10" fill="#0a6b2d">→ promote</text>
<text x="295" y="245" text-anchor="middle" font-size="10">Higher queue preempts lower (fixed priority between queues); Q0 never moves.</text></svg>"""

MLFQ_3 = f"""<svg viewBox="0 0 560 170" width="520" class="fig" font-size="11" font-family="Arial">{SVG_DEFS}
<g stroke="#222" fill="#eef3fa"><rect x="150" y="15" width="240" height="28"/><rect x="150" y="65" width="240" height="28"/><rect x="150" y="115" width="240" height="28"/></g>
<g text-anchor="middle"><text x="270" y="33">Q0 interactive: RR q = 8 ms</text><text x="270" y="83">Q1: RR q = 16 ms</text><text x="270" y="133">Q2 batch: FCFS</text></g>
<g stroke="#222" fill="none" marker-end="url(#ar)"><path d="M40,29 H148"/></g><text x="40" y="22" font-size="10">new process</text>
<g stroke="#a40000" fill="none" marker-end="url(#ar)"><path d="M390,29 H420 V79 H392"/><path d="M390,79 H420 V129 H392"/></g>
<g stroke="#0a6b2d" fill="none" marker-end="url(#ar)"><path d="M150,129 H120 V79 H148"/><path d="M150,79 H120 V35 H148"/></g>
<text x="428" y="60" font-size="10" fill="#a40000">used full quantum</text><text x="428" y="73" font-size="10" fill="#a40000">(CPU-bound) → demote</text>
<text x="2" y="100" font-size="10" fill="#0a6b2d">blocks before quantum</text><text x="2" y="113" font-size="10" fill="#0a6b2d">ends (I/O-bound) or</text><text x="2" y="126" font-size="10" fill="#0a6b2d">aging → promote</text>
<text x="270" y="162" text-anchor="middle" font-size="10">Q0 served first, then Q1, then Q2 (preemptive priority between queues)</text></svg>"""

MONITOR_SC = f"""<svg viewBox="0 0 640 300" width="600" class="fig" font-size="11" font-family="Arial">{SVG_DEFS}
<rect x="60" y="10" width="330" height="280" fill="none" stroke="#222"/>
<rect x="145" y="22" width="160" height="30" fill="#fff" stroke="#222"/><text x="225" y="42" text-anchor="middle">Entry Queue</text>
<rect x="115" y="70" width="220" height="190" fill="#fafafa" stroke="#222"/>
<rect x="135" y="80" width="180" height="40" fill="#fff" stroke="#222"/><text x="225" y="104" text-anchor="middle">Shared Data</text>
<rect x="135" y="135" width="180" height="28" fill="#fff" stroke="#222"/><text x="225" y="154" text-anchor="middle">Procedure A (q.wait)</text>
<rect x="135" y="175" width="180" height="28" fill="#fff" stroke="#222"/><text x="225" y="194" text-anchor="middle">Procedure B (q.signal)</text>
<rect x="135" y="215" width="180" height="28" fill="#fff" stroke="#222"/><text x="225" y="234" text-anchor="middle">Procedure C</text>
<rect x="68" y="120" width="40" height="110" fill="#fff" stroke="#222"/><text x="88" y="168" text-anchor="middle" font-size="9">Wait</text><text x="88" y="180" text-anchor="middle" font-size="9">Queue</text><text x="88" y="192" text-anchor="middle" font-size="9">(q)</text>
<rect x="342" y="120" width="44" height="110" fill="#fff" stroke="#222"/><text x="364" y="162" text-anchor="middle" font-size="9">Signal</text><text x="364" y="174" text-anchor="middle" font-size="9">Queue</text><text x="364" y="186" text-anchor="middle" font-size="9">(signaled,</text><text x="364" y="198" text-anchor="middle" font-size="9">re-entry)</text>
<g stroke="#222" fill="none" marker-end="url(#ar)">
<path d="M160,52 V133"/><path d="M290,52 V173"/>
<path d="M135,145 H110"/>
<path d="M88,230 V275 H364 V232"/>
<path d="M342,150 H317"/>
<path d="M250,260 V298"/><path d="M200,260 V298"/>
</g>
<g font-weight="bold" fill="#a40000" font-size="12">
<text x="148" y="66">1</text><text x="295" y="66">3</text><text x="117" y="140">2</text>
<text x="220" y="272">4</text><text x="325" y="145">6</text><text x="255" y="292">5</text><text x="186" y="292">7</text></g>
<g font-size="10.5">
<text x="400" y="30">1. Thread A enters the monitor</text>
<text x="400" y="47">2. A waits on q → q's wait queue</text>
<text x="415" y="60">(monitor released)</text>
<text x="400" y="77">3. Thread B enters the monitor</text>
<text x="400" y="94">4. B signals q: A is moved from</text>
<text x="415" y="107">wait queue → signal queue;</text>
<text x="415" y="120" font-weight="bold">B CONTINUES running</text>
<text x="400" y="137">5. B leaves the monitor</text>
<text x="400" y="154">6. A re-enters the monitor (signal</text>
<text x="415" y="167">queue has priority over entry queue)</text>
<text x="400" y="184">7. A leaves the monitor</text>
<text x="400" y="201">8. Another process can be admitted</text>
<text x="415" y="214">from the entry queue</text>
<text x="400" y="240" fill="#0b4f8a">Difference from Hoare: signal queue</text>
<text x="400" y="253" fill="#0b4f8a">now holds the SIGNALED process, not</text>
<text x="400" y="266" fill="#0b4f8a">the signaler; 8 steps instead of 9.</text></g></svg>"""

INTEL = f"""<svg viewBox="0 0 680 235" width="640" class="fig" font-size="10.5" font-family="Arial">{SVG_DEFS}
<rect x="5" y="25" width="45" height="30" fill="#eef3fa" stroke="#222"/><text x="27" y="44" text-anchor="middle">CPU</text>
<text x="70" y="18">logical address</text>
<rect x="65" y="25" width="70" height="30" fill="#fff" stroke="#222"/><rect x="135" y="25" width="60" height="30" fill="#fff" stroke="#222"/>
<text x="100" y="38" text-anchor="middle" font-size="9">selector</text><text x="100" y="50" text-anchor="middle" font-size="8">s(13) g(1) p(2)</text><text x="165" y="44" text-anchor="middle">offset 32</text>
<rect x="65" y="80" width="130" height="50" fill="#fffbe6" stroke="#222"/><text x="130" y="98" text-anchor="middle">descriptor table</text><text x="130" y="111" text-anchor="middle" font-size="9">(LDT if g=0, GDT if g=1)</text><text x="130" y="123" text-anchor="middle" font-size="9">entry = base, limit, rights</text>
<circle cx="250" cy="105" r="13" fill="#fff" stroke="#222"/><text x="250" y="110" text-anchor="middle" font-size="14">+</text>
<text x="215" y="148" font-size="9">offset ≤ limit? else trap</text>
<rect x="300" y="90" width="60" height="30" fill="#fff" stroke="#222"/><rect x="360" y="90" width="60" height="30" fill="#fff" stroke="#222"/><rect x="420" y="90" width="70" height="30" fill="#fff" stroke="#222"/>
<text x="330" y="109" text-anchor="middle">p1 (10)</text><text x="390" y="109" text-anchor="middle">p2 (10)</text><text x="455" y="109" text-anchor="middle">d (12)</text>
<text x="330" y="83">32-bit linear address</text>
<rect x="290" y="165" width="80" height="45" fill="#fffbe6" stroke="#222"/><text x="330" y="185" text-anchor="middle">page</text><text x="330" y="198" text-anchor="middle">directory</text>
<rect x="400" y="165" width="80" height="45" fill="#fffbe6" stroke="#222"/><text x="440" y="185" text-anchor="middle">page</text><text x="440" y="198" text-anchor="middle">table</text>
<rect x="520" y="165" width="50" height="30" fill="#fff" stroke="#222"/><rect x="570" y="165" width="50" height="30" fill="#fff" stroke="#222"/>
<text x="545" y="184" text-anchor="middle">frame f</text><text x="595" y="184" text-anchor="middle">d</text><text x="530" y="158">physical address</text>
<rect x="630" y="160" width="45" height="40" fill="#eef3fa" stroke="#222"/><text x="652" y="178" text-anchor="middle" font-size="9">physical</text><text x="652" y="190" text-anchor="middle" font-size="9">memory</text>
<text x="240" y="230">CR3 → page directory</text>
<g stroke="#222" fill="none" marker-end="url(#ar)">
<path d="M50,40 H63"/><path d="M100,55 V78"/><path d="M195,105 H235"/><path d="M165,55 V70 H250 V90"/>
<path d="M263,105 H298"/><path d="M330,120 V163"/><path d="M390,120 V140 H440 V163"/><path d="M370,188 H398"/>
<path d="M480,188 H518"/><path d="M455,120 V135 H595 V163"/><path d="M620,180 H628"/><path d="M270,222 H300 V212"/></g>
<text x="200" y="125" font-size="9">base</text></svg>"""

# ----------------------------------------------------------------- answers
A = {}

A["disable_int"] = """
<p>Disabling interrupts works on a uniprocessor only for <b>trusted kernel code</b>. It is the wrong tool for <b>user-level</b> synchronization because:</p>
<ol>
<li><b>It is a privileged instruction.</b> Letting user programs execute it breaks dual-mode protection; the hardware traps if user mode tries.</li>
<li><b>The OS loses control of the CPU.</b> While interrupts are off, the <b>timer interrupt</b> cannot fire, so no preemption or context switch can happen. A buggy or malicious program could disable interrupts and never re-enable them (e.g. an infinite loop in its critical section). It would then <b>monopolize the CPU</b> and hang the whole system.</li>
<li><b>Other events are delayed or lost.</b> I/O-completion interrupts and clock ticks are postponed, so devices sit idle, the system clock drifts and response time suffers. User critical sections can be long, which makes this worse.</li>
</ol>
<p>(It also does not scale: on a multiprocessor it only stops the local CPU.) User programs should instead use OS-provided semaphores/mutexes or atomic hardware instructions such as test_and_set or swap.</p>"""

A["mt_no_better"] = """
<p>Multithreading helps only if there is work that can overlap. Two examples where it does not help:</p>
<ul>
<li>A <b>strictly sequential computation</b>, where each step depends on the previous result. Examples are computing a tax return or a recurrence such as Fibonacci with an iterative loop. There is nothing to run in parallel, and threads only add creation, context-switch and synchronization overhead.</li>
<li>A <b>CPU-bound program on a single processor</b> with no I/O (e.g. a matrix multiply). The threads just take turns on the same CPU, so the total time is the same or worse because of switching overhead.</li>
</ul>
<p>Another standard example is a shell or interactive program that only waits for one user's input. It spends its time blocked anyway.</p>"""

A["ws_atomic"] = """
<p>Busy-waiting definitions: <code>wait(S){ while (S &lt;= 0); S--; }</code> and <code>signal(S){ S++; }</code>, with S = 1 (unlocked).</p>
<p>If wait() is not atomic, the test and the decrement can be interleaved:</p>
<table><tr><th>Step</th><th>P0</th><th>P1</th><th>S</th></tr>
<tr><td>1</td><td>tests S&lt;=0 → false (S=1)</td><td></td><td>1</td></tr>
<tr><td>2</td><td><i>preempted</i></td><td>tests S&lt;=0 → false (S=1)</td><td>1</td></tr>
<tr><td>3</td><td></td><td>S-- ; enters critical section</td><td>0</td></tr>
<tr><td>4</td><td>S-- ; enters critical section</td><td></td><td>−1</td></tr></table>
<p><b>Both P0 and P1 are in the critical section, so mutual exclusion is violated.</b> Likewise, S-- and S++ are each load, modify, store at machine level. If two processes run them concurrently, an update can be lost, e.g. two signal() calls increment S only once. A lost signal can block a process forever, and an extra count lets two processes in. So wait() and signal() must be indivisible.</p>"""

A["m2m_less"] = """<p><b>Fewer kernel threads than processors.</b> The kernel can schedule only that many of the program's threads at once. Some processors are left <b>idle</b> as far as this program is concerned, and the available parallelism is wasted. Also, if a kernel thread blocks (e.g. on I/O), even fewer user threads can run.</p>"""
A["m2m_equal"] = """<p><b>Equal to the number of processors.</b> All processors can run the program's threads simultaneously, giving the best case while no thread blocks. However, when a kernel thread <b>blocks</b> (I/O, page fault, system call), its processor becomes <b>idle</b>. No spare kernel thread exists to run another ready user thread on it, so performance drops during blocking.</p>"""
A["m2m_greater"] = """<p><b>More kernel threads than processors, but fewer than user threads.</b> This gives the best utilization. When one kernel thread blocks, the kernel can schedule <b>another ready kernel thread</b> (carrying another user thread) on that processor, so CPUs stay busy. The cost is some extra kernel overhead: more kernel threads to create, schedule and context-switch.</p>"""

A["mlq_list"] = """
<p>Two ways to schedule <b>among</b> the queues of a multilevel queue:</p>
<ol>
<li><b>Fixed-priority (preemptive) scheduling.</b> Serve all processes in a higher-priority queue (e.g. foreground/interactive) before any process in a lower queue (background/batch). A process arriving in a higher queue preempts a lower one. Lower queues may <b>starve</b>.</li>
<li><b>Time slicing among queues.</b> Each queue gets a fixed share of CPU time, which it schedules among its own processes. Example: 80% to the foreground queue (RR) and 20% to the background queue (FCFS).</li>
</ol>"""

A["linux_mlq"] = """
<p><b>Fixed priority between classes.</b> Linux has two priority ranges mapped onto one global scale (lower number = higher priority). <b>Real-time</b> tasks are 0–99 and use POSIX SCHED_FIFO / SCHED_RR with static priorities. <b>Normal (time-sharing)</b> tasks are 100–139, from nice −20…+19. A runnable real-time task always runs before any normal task, which is fixed-priority scheduling between the two "queues". With CFS, the scheduler likewise picks the highest-priority <b>scheduling class</b> first (real-time class before the default class).</p>
<p><b>Time slicing.</b> In the O(1) scheduler (2.5) each task gets a time slice based on priority, and higher priority gets a longer quantum. Each CPU's runqueue has an <b>active</b> and an <b>expired</b> priority array. A task runs while it has slice left, then moves to expired. When the active array is empty, the arrays are <b>swapped</b>, so every task gets its share. In CFS (2.6.23+), instead of fixed quanta each task gets a <b>proportion</b> of CPU time within a <b>target latency</b>, weighted by nice value. The task with the smallest <b>virtual runtime (vruntime)</b> runs next. This is proportional sharing of time.</p>"""

A["bits_logical"] = """<p>Pages: 64 = 2<sup>6</sup> gives a 6-bit page number. Page size: 1024 = 2<sup>10</sup> words gives a 10-bit offset.<br><b>Logical address = 6 + 10 = 16 bits.</b></p>"""
A["bits_physical"] = """<p>Frames: 32 = 2<sup>5</sup> gives a 5-bit frame number. The frame size equals the page size (2<sup>10</sup>), so the offset is 10 bits.<br><b>Physical address = 5 + 10 = 15 bits.</b></p>"""

MON_STATE_HDR = "<tr><th>Active in M</th><th>Entry queue</th><th>Signal queue</th><th>x queue</th><th>y queue</th></tr>"
A["mon_p7"] = f"""<p>P7 just joins the end of the entry queue. Nothing else changes.</p>
<table>{MON_STATE_HDR}<tr><td>P0</td><td>P1, P2, <b>P7</b></td><td>P3</td><td>P4, P5</td><td>P6</td></tr></table>"""
A["mon_xsig"] = f"""<p>Signal-and-wait (Hoare): the first waiter on x, <b>P4, resumes immediately</b>. The signaler <b>P0 is suspended in the signal queue</b>.</p>
<table>{MON_STATE_HDR}<tr><td><b>P4</b></td><td>P1, P2</td><td>P3, <b>P0</b></td><td>P5</td><td>P6</td></tr></table>"""
A["mon_ywait"] = f"""<p>P0 joins y's queue and releases the monitor. The signal queue has priority over the entry queue, so <b>P3 becomes active</b>.</p>
<table>{MON_STATE_HDR}<tr><td><b>P3</b></td><td>P1, P2</td><td>(empty)</td><td>P4, P5</td><td>P6, <b>P0</b></td></tr></table>"""

A["c_util_resp"] = """<p><b>CPU utilization vs. response time.</b> CPU utilization is highest when context switches are rare, as with FCFS or a long quantum, because each switch is pure overhead. Good response time for interactive users needs <b>frequent preemption</b> (a short RR quantum) so every user gets the CPU quickly. That causes many context switches, so the CPU spends more time switching and less doing useful work, which lowers utilization.</p>"""
A["c_turn_wait"] = """<p><b>Average turnaround time vs. maximum waiting time.</b> Average turnaround is minimized by running the <b>shortest jobs first</b> (SJF/SRTF). But a long job can be postponed again and again as short jobs keep arriving, so it may <b>starve</b>. Its waiting time, the <b>maximum</b> waiting time, becomes very large (unbounded). Bounding the maximum wait (e.g. with FCFS or aging) raises the average turnaround.</p>"""
A["c_io_cpu"] = """<p><b>I/O device utilization vs. CPU utilization.</b> Keeping devices busy means running <b>I/O-bound</b> processes as soon as their I/O completes, so they can issue the next request quickly. This means frequently preempting CPU-bound processes, and the context-switch overhead lowers CPU utilization. Maximizing CPU utilization means letting CPU-bound jobs run long without switching, which leaves the I/O devices <b>idle</b> while I/O-bound jobs wait for the CPU.</p>"""
A["c_dead_fair"] = """<p><b>Deadline vs. fairness.</b> To meet deadlines, the scheduler must always give the CPU to the most urgent process (earliest deadline or real-time priority), regardless of how much CPU it has already had. Other processes may wait a long time or <b>starve</b>, which is unfair. A <b>fair</b> scheduler gives everyone an equal share, so urgent tasks may not get enough CPU in time and <b>miss their deadlines</b>.</p>"""
A["c_thru_cs"] = """<p><b>Throughput vs. context-switch overhead.</b> Throughput (jobs completed per unit time) is improved by finishing short jobs quickly, which needs preemption: SJF/SRTF or a small RR quantum. Every preemption adds <b>context-switch overhead</b>, during which no useful work is done. Minimizing switches (FCFS, large quantum) traps short jobs behind long ones (<b>convoy effect</b>), so fewer jobs complete per unit time. If the quantum is too small, overhead itself eats the throughput.</p>"""

A["busywait_deadlock"] = """
<p><b>Busy waiting</b> (spinning) means a process waiting to enter its critical section repeatedly executes a loop that tests a condition, e.g. <code>while (test_and_set(&amp;lock));</code> or <code>while (S &lt;= 0);</code>. It never gives up the CPU while waiting.</p>
<p><b>Performance:</b> the spinning process <b>wastes CPU cycles</b> that other processes could use. On a uniprocessor this is even worse: the spinner burns its whole time slice, and the lock holder cannot run during that time to finish and release the lock. So waiting gets longer and throughput drops.</p>
<p><b>Deadlock:</b> with priority scheduling, suppose a high-priority process H spins on a lock held by a low-priority process L. H is always runnable, so the scheduler never runs L. L can never release the lock, and H spins forever. Both are stuck (a priority-inversion deadlock).</p>
<p>Fix: a blocking semaphore, where a waiting process sleeps on a queue instead of spinning.</p>"""

A["busywait"] = """
<p><b>Busy waiting</b> (spinning) means a process waiting to enter its critical section stays in a loop that keeps testing a condition until it can enter, e.g. <code>while (test_and_set(&amp;lock));</code> or <code>while (S &lt;= 0);</code>. It never gives up the CPU while waiting.</p>
<p><b>Degraded performance:</b> the waiting process <b>wastes CPU cycles</b> doing no useful work, and other ready processes could have used them. On a single CPU, the spinner uses its entire time slice while the lock holder cannot run to release the lock, so everyone waits longer. If the spinner has higher priority than the lock holder, the holder may never run, and the system can even <b>deadlock</b> (priority inversion). Busy waiting is acceptable only for very short waits on multiprocessors, where it avoids a context switch.</p>"""

A["sem_block"] = """
<p>Each semaphore has an integer value and a <b>queue of waiting processes</b>. Instead of spinning, a process that must wait is <b>blocked</b> (moved to the waiting state and placed on the semaphore's queue). <code>signal</code> <b>wakes up</b> one waiting process (moves it to the ready queue).</p>""" + code("""
typedef struct {
    int value;
    struct process *list;  /* queue of waiting PCBs */
} semaphore;

void wait(semaphore *S) {
    S->value--;
    if (S->value < 0) {
        add this process to S->list;
        block();               /* running -> waiting */
    }
}

void signal(semaphore *S) {
    S->value++;
    if (S->value <= 0) {
        remove a process P from S->list;
        wakeup(P);             /* waiting -> ready */
    }
}
""") + """<p>If value is negative, |value| is the number of waiting processes. block() and wakeup() are system calls. wait() and signal() must still be atomic: disable interrupts inside them on a uniprocessor, or use a spinlock on a multiprocessor. That busy wait is limited to these few instructions, so it is short and rare.</p>"""

A["bounded_sem"] = """
<p>Three semaphores protect a buffer of <i>n</i> slots: <b>mutex = 1</b> (mutual exclusion on the buffer), <b>empty = n</b> and <b>full = 0</b>.</p>
<ul>
<li><b>empty</b> counts <b>empty slots</b>. The producer calls <code>wait(empty)</code> before inserting, so it blocks when the buffer is full. The consumer calls <code>signal(empty)</code> after removing an item.</li>
<li><b>full</b> counts <b>filled slots</b>. The consumer calls <code>wait(full)</code> before removing, so it blocks when the buffer is empty. The producer calls <code>signal(full)</code> after inserting.</li>
</ul>""" + code("""
Producer:                        Consumer:
do {                             do {
    /* produce item */               wait(full);
    wait(empty);                     wait(mutex);
    wait(mutex);                     /* remove item */
    /* add item to buffer */         signal(mutex);
    signal(mutex);                   signal(empty);
    signal(full);                    /* consume item */
} while (true);                  } while (true);
""") + """<p>Together they replace busy-wait loops, so all n slots can be used. Order matters: calling wait(mutex) before wait(empty) can deadlock.</p>"""

A["util_thru"] = """
<p>CPU utilization measures how busy the CPU is; throughput measures how many processes <b>complete</b> per unit time. Maximizing one can hurt the other:</p>
<ul>
<li>Running <b>long CPU-bound jobs</b> keeps the CPU near 100% busy (high utilization). But each job takes a long time, so <b>few jobs finish</b> per unit time (low throughput). Short jobs stuck behind them also delay completion (convoy effect).</li>
<li>Favoring <b>many short jobs</b> (SJF, short quantum) completes more jobs per unit time (high throughput). But it causes more context switches, whose overhead is not useful work, and short I/O-bound jobs leave the CPU idle while they wait on I/O. So utilization drops.</li>
</ul>"""

A["fork_exec_mt"] = """
<p><b>fork():</b> this depends on the system. Some UNIX systems provide <b>two versions</b> of fork(). One <b>duplicates all threads</b> of the process. The other (the POSIX behaviour) <b>duplicates only the thread that called fork()</b>, so the child is single-threaded. If exec() is called right after fork(), duplicating only the calling thread is enough, because exec replaces everything anyway. If the child does not call exec, duplicating all threads may be needed.</p>
<p><b>exec():</b> exec works as usual. The program named in its parameter <b>replaces the entire process, including all of its threads</b>. The other threads are destroyed, and the new program starts with a single thread.</p>"""

A["regressive"] = """
<p><b>It favors CPU-bound processes.</b></p>
<ul>
<li>A process that <b>uses its entire quantum</b> (does not block for I/O) is CPU-bound behaviour. It is <b>rewarded</b>: +10 ms of quantum, up to 100 ms, <b>and</b> a priority boost.</li>
<li>A process that <b>blocks before using its quantum</b> is I/O-bound / interactive behaviour. It is <b>penalized</b>: −5 ms of quantum, and its priority is <b>not</b> raised.</li>
</ul>
<p>So over time CPU-bound (batch) processes get longer time slices and higher priority, and I/O-bound processes get shorter slices and stay at lower priority. This is the opposite of the usual goal of favoring interactive processes.</p>"""

A["m2one_mp"] = """
<p><b>No, not significantly.</b> In the many-to-one model, all user-level threads of the process are mapped onto <b>one kernel thread</b>. The kernel schedules only kernel threads, so it sees the process as a single schedulable entity. It can run on only <b>one processor at a time</b>, which means only one user thread executes at any moment even if other CPUs are idle. The program gets <b>no parallelism</b>, and its performance is essentially the same as on a single processor. Also, if any thread makes a blocking system call, the whole process (all threads) blocks.</p>
<p>(The only gain is indirect: other processes can use the other CPUs, so the program may face less competition.) To benefit from multiple processors you need one-to-one or many-to-many threading.</p>"""

A["mlq_why"] = """
<p>I/O-bound and CPU-bound processes behave very differently. <b>I/O-bound</b> processes have many short CPU bursts. <b>CPU-bound</b> processes have few, long bursts.</p>
<ul>
<li>If an I/O-bound process gets the CPU quickly, it issues its next I/O request soon and then gets out of the way. The <b>devices stay busy</b> while CPU-bound processes use the CPU, so <b>both CPU and I/O utilization</b> improve.</li>
<li>I/O-bound processes are usually <b>interactive</b>, so serving them first gives good <b>response time</b>.</li>
<li>If they wait behind long CPU bursts (convoy effect), devices go idle and users see poor response.</li>
</ul>
<p>So the scheduler should give I/O-bound processes higher priority and short quanta, and give CPU-bound processes lower priority with longer quanta (fewer switches).</p>"""

A["mlq_modify3"] = """
<p>Change it into a <b>multilevel feedback queue</b>, where a process can <b>move between queues</b> based on its observed CPU bursts:</p>""" + MLFQ_3 + """
<ul>
<li>A new process enters <b>Q0</b> (small quantum). If it <b>uses the full quantum</b>, it is behaving CPU-bound and is <b>demoted</b> to Q1, then to Q2.</li>
<li>If it <b>blocks for I/O before its quantum expires</b>, it is I/O-bound and stays in, or is <b>promoted</b> to, a higher queue.</li>
<li><b>Aging:</b> a process that waits too long in a low queue is moved up, which prevents starvation.</li>
</ul>
<p>So I/O-bound processes end up in high-priority, short-quantum queues and CPU-bound processes in low-priority, long-quantum queues. Parameters: number of queues, algorithm per queue, promotion rule, demotion rule, entry queue.</p>"""

A["mlq_modify5"] = """
<p>Turn it into a <b>multilevel feedback queue</b>: a process may <b>move between queues</b> according to its observed behaviour, so it reaches the right queue automatically after a few runs.</p>""" + MLFQ_5 + """
<ul>
<li>A new process enters the <b>interactive</b> queue of its class (faculty → Q1, student → Q2), which uses a short quantum.</li>
<li>If it <b>uses its whole quantum</b>, it is CPU-bound, so it is <b>demoted</b> to the batch queue of its class (Q1→Q3, Q2→Q4).</li>
<li>If it <b>blocks for I/O before the quantum ends</b>, it is interactive, so it stays in or is <b>promoted</b> back to the interactive queue (Q3→Q1, Q4→Q2).</li>
<li><b>Aging</b> promotes processes that wait too long, preventing starvation. System processes stay fixed in Q0.</li>
</ul>
<p>Defined by: number of queues, scheduling algorithm per queue, when to promote, when to demote, and which queue a new process enters.</p>"""

A["tas"] = code("""
boolean test_and_set(boolean *target) {   /* executed ATOMICALLY by hardware */
    boolean rv = *target;
    *target = true;
    return rv;
}

boolean lock = false;                     /* shared */

do {
    while (test_and_set(&lock))
        ;                                 /* spin while lock was already true */
    /* critical section */
    lock = false;                         /* release */
    /* remainder section */
} while (true);
""") + """<p>The first process to call test_and_set gets back <b>false</b> (the lock was free) and has atomically set lock to true, so it enters. Every other caller gets <b>true</b> and keeps looping until the holder sets lock = false. This gives mutual exclusion. (Bounded waiting needs an extra <code>waiting[]</code> array.)</p>"""

A["tas_fail"] = """
<p>If test_and_set is not atomic, its read (<code>rv = *target</code>) and write (<code>*target = true</code>) can be interleaved. Start with lock = false:</p>
<table><tr><th>Step</th><th>P0</th><th>P1</th><th>lock</th></tr>
<tr><td>1</td><td>rv = lock → false</td><td></td><td>false</td></tr>
<tr><td>2</td><td><i>preempted</i></td><td>rv = lock → false</td><td>false</td></tr>
<tr><td>3</td><td></td><td>lock = true; returns false → <b>enters CS</b></td><td>true</td></tr>
<tr><td>4</td><td>lock = true; returns false → <b>enters CS</b></td><td></td><td>true</td></tr></table>
<p>Both processes saw the lock as free, so <b>both are in the critical section: mutual exclusion is violated.</b></p>"""

A["swap"] = code("""
/* swap: executed ATOMICALLY by hardware */
void swap(boolean *a, boolean *b) {
    boolean temp = *a;
    *a = *b;
    *b = temp;
}

boolean lock = false;           /* shared */
boolean key;                    /* local to each process */

do {
    key = true;
    while (key == true)
        swap(&lock, &key);  /* key=old lock; lock=true */
    /* critical section */
    lock = false;
    /* remainder section */
} while (true);
""") + """<p>A process loops until a swap returns <b>key = false</b>, meaning the lock was free. That same swap atomically set lock = true, so only one process gets out of the loop. The others keep getting key = true until lock is reset to false.</p>"""

A["swap_fail"] = """
<p>If swap is not atomic, the three steps (<code>temp=*a; *a=*b; *b=temp</code>) of two processes can interleave. Start with lock = false, and each process has key = true:</p>
<table><tr><th>Step</th><th>P0</th><th>P1</th><th>lock</th></tr>
<tr><td>1</td><td>temp0 = lock → false</td><td></td><td>false</td></tr>
<tr><td>2</td><td><i>preempted</i></td><td>temp1 = lock → false</td><td>false</td></tr>
<tr><td>3</td><td></td><td>lock = key1 (true); key1 = temp1 = false → <b>enters CS</b></td><td>true</td></tr>
<tr><td>4</td><td>lock = key0 (true); key0 = temp0 = false → <b>enters CS</b></td><td></td><td>true</td></tr></table>
<p>Both read the old value false before either wrote true, so both leave the loop. <b>Mutual exclusion is violated.</b></p>"""

A["race_bank"] = """
<p>deposit() does <code>balance = balance + amount</code> and withdraw() does <code>balance = balance - amount</code>. At machine level each is <b>load balance → modify in a register → store balance</b>, which is not atomic. Suppose balance = 100, the husband withdraws 50 and the wife deposits 50 (the correct result is 100):</p>
<table><tr><th>Step</th><th>Husband: withdraw(50)</th><th>Wife: deposit(50)</th><th>balance</th></tr>
<tr><td>1</td><td>reg1 = balance (100)</td><td></td><td>100</td></tr>
<tr><td>2</td><td></td><td>reg2 = balance (100)</td><td>100</td></tr>
<tr><td>3</td><td>reg1 = 100 − 50; balance = 50</td><td></td><td>50</td></tr>
<tr><td>4</td><td></td><td>reg2 = 100 + 50; balance = 150</td><td><b>150</b></td></tr></table>
<p>The withdrawal is lost, and the result would be 50 if steps 3 and 4 were swapped. The outcome depends on the order of execution, which is a <b>race condition</b>.</p>
<p><b>Prevention:</b> make the update a critical section, so only one method can touch balance at a time. Use a lock or semaphore (<code>wait(mutex); balance ±= amount; signal(mutex);</code>), a monitor, or synchronized methods.</p>"""

A["forkcount"] = """
<p>Trace each fork (the original process is P0):</p>
<ul>
<li>fork ① gives P0 and child C1. Only C1 has pid == 0.</li>
<li>Inside the if, C1 calls fork ②, creating C2. <b>C1 and C2 each call thread_create()</b>, so 2 threads are created.</li>
<li>The final fork ③ is executed by P0, C1 and C2, creating C3, C4 and C5.</li>
</ul>""" + FORK_TREE + """
<p><b>(a) 6 unique processes</b> (P0, C1–C5; 5 newly created if the original is not counted).<br>
<b>(b) 2 unique threads</b> created by thread_create(), one in C1 and one in C2. The last fork() duplicates only the calling thread (POSIX), so it creates no extra threads.</p>"""

A["exec_before_fork"] = """
<p>exec() <b>replaces the calling process's entire memory image</b> (code, data, heap, stack) with the program named in its parameters. On success, <b>it never returns</b>.</p>
<p>So if exec() is placed before fork(), the new program starts running in place of the original one, under the <b>same process ID</b>. The rest of the original code, <b>including the fork() call, is gone and never executed</b>. <b>No child process is created</b>, and the original program's remaining work is not done.</p>
<p>Only if exec() <b>fails</b> (returns −1) does execution continue to the fork().</p>"""

A["affinity"] = """
<p><b>Processor affinity:</b> a process has an affinity for the processor it is currently running on. It is kept on (or restricted to) that same CPU rather than migrated to another one.</p>
<p><b>Why it matters on multiple-CPU systems:</b> while a process runs, its recently used data fills that processor's <b>cache</b>. If the scheduler migrates it to another CPU, the old cache contents must be <b>invalidated</b> and the new processor's cache must be <b>repopulated</b>. That causes many cache misses and memory stalls, which is expensive. Keeping the process on the same CPU reuses the "warm" cache. On NUMA systems it also keeps the process close to its local memory.</p>
<p><b>Soft affinity:</b> the OS tries to keep the process on the same CPU but may migrate it. <b>Hard affinity:</b> the process specifies the set of CPUs it may run on. The scheduler must balance affinity against <b>load balancing</b> (push/pull migration), which moves processes from busy to idle CPUs.</p>"""

A["lottery"] = """
<p>Give <b>higher-priority threads more lottery tickets</b>. At each of the 50 drawings per second, the winning ticket is chosen uniformly at random. A thread holding <i>k</i> of the <i>T</i> tickets therefore wins with probability k/T, and on average receives about <b>k/T of the CPU time</b> (k/T × 50 × 20 ms per second).</p>
<p>Example: high-priority thread H has 30 tickets and low-priority L has 10. H wins about 75% of the drawings (≈ 750 ms per second) and L about 25% (≈ 250 ms). The scheduler can also adjust priority dynamically by giving or taking away tickets, e.g. extra tickets to a thread that has waited long. Every thread with at least one ticket eventually wins, so there is no starvation.</p>"""

A["hoare_sc"] = """
<p><b>Signal-and-continue:</b> when B executes <code>q.signal()</code>, <b>B keeps running</b> in the monitor. The waiting process A is only moved from q's wait queue to a ready/re-entry queue (the "signal queue" now holds the <i>signaled</i> process). A resumes after B leaves the monitor or waits.</p>""" + MONITOR_SC + """
<p>Compared with Hoare: in Hoare's version A runs immediately and the signaler B waits in the signal queue. In signal-and-continue, A may find the condition changed by the time it runs, so waiters should re-check it with <code>while (!cond) q.wait();</code>. There are fewer context switches, and this is what Java and Pthreads use.</p>"""

A["sc_sem"] = """
<p>In signal-and-wait the <b>signaler</b> blocks on <code>next</code>. For <b>signal-and-continue</b>, the signaler must <b>not</b> block. Instead, the <b>signaled</b> process waits on <code>next</code> to re-enter after the signaler leaves. Changed lines are marked NEW:</p>""" + code("""
Variables
    semaphore mutex;      // (initially = 1)
    semaphore next;       // (initially = 0)
                          // = signaled procs
                          //   waiting to re-enter
    int next_count = 0;

Each procedure F (unchanged)
    wait(mutex);
        ...
        // body of F;
        ...
    if (next_count > 0)
        signal(next);     // signaled proc first
    else
        signal(mutex);

For each condition variable x
    semaphore x_sem;      // (initially = 0)
    int x_count = 0;

x.wait
    x_count++;
    if (next_count > 0)
        signal(next);
    else
        signal(mutex);
    wait(x_sem);          // sleep until signaled
    wait(next);           // NEW: wait until the
                          //   signaler leaves/waits
    next_count--;         // NEW: back in monitor
                          // (x_count-- moved to
                          //   x.signal)

x.signal                  // signal-and-continue
    if (x_count > 0) {
        x_count--;        // NEW: done by signaler
        next_count++;
        signal(x_sem);    // wake one waiter
        // REMOVED: wait(next); next_count--;
    }                     // signaler continues
""") + """<p>Why: the signaler no longer suspends itself. The woken process must re-acquire the monitor, and it gets it through <code>next</code>, ahead of the entry queue, when the signaler exits or waits. x_count is decremented by the signaler, so two consecutive signals cannot wake the same single waiter twice. Callers should use <code>while (!B) x.wait();</code>.</p>"""

A["dp_sc"] = """
<p>Combine the dining-philosopher monitor with the signal-and-continue implementation above. <code>self[i]</code> becomes semaphore <code>self_sem[i]</code> plus counter <code>self_count[i]</code>.</p>""" + code("""
enum {THINKING, HUNGRY, EATING} state[5];
semaphore mutex = 1;             // monitor lock
semaphore next  = 0;      // signaled, waiting to re-enter
int next_count  = 0;
semaphore self_sem[5]   = {0,0,0,0,0};  // cond. self[i]
int       self_count[5] = {0,0,0,0,0};

void leave() {                // release the monitor
    if (next_count > 0) signal(next);
    else                signal(mutex);
}
void self_wait(int i) {          // self[i].wait()
    self_count[i]++;
    leave();                  // release monitor
    wait(self_sem[i]);           // sleep until signaled
    wait(next);               // re-enter after signaler
    next_count--;
}
void self_signal(int i) {     // self[i].signal(), S&C
    if (self_count[i] > 0) {
        self_count[i]--;
        next_count++;
        signal(self_sem[i]);  // wake i; caller continues
    }
}
void test(int i) {            // only inside the monitor
    if (state[(i+4)%5] != EATING && state[i] == HUNGRY &&
        state[(i+1)%5] != EATING) {
        state[i] = EATING;
        self_signal(i);
    }
}
void pickup(int i) {
    wait(mutex);                 // enter monitor
    state[i] = HUNGRY;
    test(i);
    while (state[i] != EATING)  // re-check after waking
        self_wait(i);
    leave();
}
void putdown(int i) {
    wait(mutex);                 // enter monitor
    state[i] = THINKING;
    test((i+4)%5);            // left neighbor may eat
    test((i+1)%5);            // right neighbor may eat
    leave();
}
void init() {
    for (int i = 0; i < 5; i++) state[i] = THINKING;
}

void philosopher(int i) {
    while (true) {
        think(); pickup(i); eat(); putdown(i);
    }
}
""") + """<p>It is correct under signal-and-continue because test() sets state[i] = EATING <b>before</b> signaling, and only philosopher i can change it back. So when i resumes, its condition still holds. A philosopher eats only when neither neighbor eats, so there is no deadlock (starvation is still possible).</p>"""

A["pthread"] = """
<p><b>Incorrect.</b> Problems:</p>
<ol>
<li><b>All 100 threads receive the same address <code>&amp;param1</code>.</b> main keeps incrementing param1 while the threads run, so each thread prints whatever value param1 holds when that thread happens to run. The output has duplicates and missing numbers (often many 100s), not 1…100.</li>
<li>main never calls <b>pthread_join</b>, so it may return (ending the process and all its threads) before the threads print.</li>
<li><code>*y</code> dereferences a <code>void *</code>, so it needs a cast to <code>int *</code>.</li>
</ol>
<p><b>Corrected:</b> give every thread its own argument and join all threads.</p>""" + code("""
void *doSomething(void *y) {
    ...
    printf("%d\\n", *(int *)y);
    ...
    pthread_exit(0);
}

int main() {
    pthread_t t1[100];            /* declare threads */
    int param[100], i;      /* one argument per thread */

    for (i = 0; i < 100; i++) {
        param[i] = i + 1;         /* 1, 2, ..., 100 */
        pthread_create(&(t1[i]), NULL, doSomething, &param[i]);
    }
    for (i = 0; i < 100; i++)
        pthread_join(t1[i], NULL);  /* wait for all */
    return 0;
}
""") + """<p>(If the numbers must also be printed <i>in order</i>, the threads must additionally be synchronized, e.g. by joining each thread right after creating it.)</p>"""

A["intel_steps"] = INTEL + """
<ol>
<li>The CPU generates a <b>logical address = (selector, offset)</b>. The 16-bit selector has <b>s</b> = 13-bit segment number, <b>g</b> = 1 bit choosing GDT or LDT, and <b>p</b> = 2 protection bits.</li>
<li>The <b>segmentation unit</b> uses s and g to fetch the 8-byte <b>segment descriptor</b> from the <b>LDT</b> (private segments) or <b>GDT</b> (shared segments). Descriptors are cached in segment registers. It checks the offset against the segment <b>limit</b> and the access rights, trapping on a violation, then computes the <b>linear address = base + offset</b> (32 bits).</li>
<li>The <b>paging unit</b> splits the linear address into <b>p1 (10 bits) | p2 (10 bits) | d (12 bits)</b>. Register <b>CR3</b> points to the current <b>page directory</b>. p1 selects a directory entry, which points to a <b>page table</b>. p2 selects the page-table entry, which gives <b>frame f</b>.</li>
<li><b>Physical address = f concatenated with d</b>, which is sent to memory. (For 4 MB pages the directory entry points straight at the frame, with a 22-bit offset. The TLB caches recent translations.)</li>
</ol>"""

A["intel_adv"] = """
<ul>
<li><b>Segmentation</b> matches the programmer's view (code, data and stack as separate logical units). It gives <b>per-segment protection</b> (e.g. read-only, execute-only code, privilege levels) and easy <b>sharing</b> of whole segments between processes.</li>
<li><b>Paging</b> on top removes <b>external fragmentation</b>. Segments need not be contiguous in physical memory; they are allocated in fixed-size frames, so allocation is simple.</li>
<li>The OS gets <b>flexibility</b>: pages can be swapped or loaded on demand (virtual memory), shared at page level, and protected with page bits. The hardware does the work at memory speed, so the OS does not translate in software.</li>
</ul>"""

A["intel_disadv"] = """
<p><b>Yes.</b></p>
<ul>
<li><b>Slower access:</b> without TLB hits, each reference needs a segment-descriptor lookup plus <b>two page-table memory accesses</b> (directory and table) before the data access itself.</li>
<li><b>Complexity and cost:</b> more hardware (segment registers, descriptor tables, MMU, TLB), more chip area and power. The OS must manage both segment tables and page tables.</li>
<li><b>Memory overhead</b> for the tables, and paging still has internal fragmentation.</li>
</ul>
<p>Because of this cost and complexity, many manufacturers (most RISC designs, ARM, and x86-64 in practice with a flat segment model) use <b>paging only</b>. It delivers most of the benefit with simpler, faster hardware.</p>"""

A["demand_paging"] = """
<p>Let p = page-fault rate. Memory access = 100 ns. A page-fault service averages:</p>
<p>0.3 × 8 ms + 0.7 × 20 ms = 2.4 + 14 = <b>16.4 ms = 16,400,000 ns</b></p>
<p>Effective access time: EAT = (1 − p) × 100 + p × 16,400,000 ≤ 200</p>
<p>100 + 16,399,900 p ≤ 200 → p ≤ 100 / 16,399,900</p>
<p><b>p ≤ 6.1 × 10<sup>−6</sup></b> (about 1 fault per 164,000 memory accesses).</p>
<p class="note">Keep units consistent (ms → ns). Since the page table is in registers, a non-faulting access costs just one memory access (100 ns).</p>"""

A["socket"] = """
<ul>
<li>A <b>PID is assigned dynamically</b> by the local OS. It changes every time the server is restarted and is <b>unique only within one host</b>, so a client on another machine cannot know or rely on it.</li>
<li>A <b>port number is fixed and well known</b>, tied to a <b>service</b> rather than to a particular process (e.g. HTTP = 80, SSH = 22; ports below 1024 are reserved). A client can find a service just from IP address and port. A socket is identified by <b>IP:port</b>, e.g. 161.25.19.8:1625.</li>
<li>The process behind a service can change (restart, failover, a pool of worker processes or threads) and one process may offer several services. The port stays the same, and the network stack uses it to deliver packets to the right endpoint.</li>
</ul>"""

A["buffer_n1"] = """
<p>The solution uses only <code>in</code> (next free slot) and <code>out</code> (next full slot) to describe the buffer state, and it defines <b>empty</b> as <code>in == out</code> (consumer waits).</p>
<p>If the producer were allowed to fill <b>all</b> BUFFER_SIZE slots, then after the last insert <code>in</code> would wrap around and also equal <code>out</code>. <b>"Full" would look exactly like "empty"</b>, and the consumer could not tell them apart. To avoid this ambiguity, the producer treats the buffer as <b>full when <code>(in + 1) % BUFFER_SIZE == out</code></b>, so one slot is always left unused.</p>
<p>Example with BUFFER_SIZE = 10: out = 0 and the producer has filled b0–b8, so in = 9. Now (9+1) % 10 = 0 = out, and the producer waits with only <b>9 items</b> stored. b9 stays empty; filling it would make in = 0 = out, which means "empty".</p>
<p>To use all N slots, add a <code>counter</code> of items (which then needs synchronization because counter++/counter-- race) or a full/empty flag.</p>"""

A["rms"] = """
<p>CPU utilization U = 25/50 + 30/75 = 0.50 + 0.40 = <b>0.90</b>. The RMS guaranteed bound for N = 2 is 2(2<sup>1/2</sup> − 1) ≈ <b>0.83</b>. Since U &gt; 0.83, schedulability is not guaranteed, so draw the chart. RMS uses static priority by period: P1 (period 50) has <b>higher priority</b> than P2 (period 75).</p>""" + gantt([("P1", 0, 25, "g1"), ("P2 (25 of 30)", 25, 50, "g2"), ("P1", 50, 75, "g1"), ("P2 misses deadline", 75, 100, "gx")], 100) + """
<ul><li>0–25: P1 runs (deadline 50 met).</li>
<li>25–50: P2 runs, but at t = 50 P1's second period starts and, having higher priority, <b>preempts P2</b>. P2 has done only 25 of its 30 ms.</li>
<li>50–75: P1 runs (deadline 100 met).</li>
<li>t = 75: P2's deadline arrives with 5 ms still left, so <b>P2 misses its deadline</b>.</li></ul>
<p><b>No, P1 and P2 cannot be scheduled with RMS.</b></p>"""

A["edf"] = """
<p>EDF assigns priority dynamically: the job with the <b>earliest absolute deadline</b> runs (on a tie, the running job continues). U = 0.90 ≤ 1, so EDF can schedule them.</p>""" + gantt([("P1", 0, 25, "g1"), ("P2", 25, 55, "g2"), ("P1", 55, 80, "g1"), ("P2", 80, 110, "g2"), ("P1", 110, 135, "g1"), ("idle", 135, 150, "gi")], 150) + """
<ul>
<li>t=0: P1 (deadline 50) vs P2 (deadline 75), so P1 runs 0–25. Then P2 starts at 25.</li>
<li>t=50: P1's 2nd job arrives (deadline 100). P2's deadline 75 is earlier, so <b>P2 is not preempted</b> and finishes at 55 (deadline 75 met). P1 runs from 55.</li>
<li>t=75: P2's 2nd job arrives (deadline 150). P1's deadline 100 is earlier, so P1 finishes at 80 (met). P2 runs 80–110.</li>
<li>t=100: P1's 3rd job (deadline 150) ties with P2, so no preemption. P2 finishes at 110 (met), and P1 runs 110–135 (met). Idle 135–150.</li>
<li>At t = 150 (LCM of 50 and 75) both tasks restart, so the pattern repeats.</li>
</ul>
<p><b>All deadlines are met under EDF.</b></p>"""

A["paging48"] = """
<p><b>Memory space per process:</b> 48-bit addresses give 2<sup>48</sup> bytes = <b>256 TB</b> of logical address space.</p>
<p><b>Page-table entries:</b> 4 KB = 2<sup>12</sup> gives a 12-bit offset, so the page number is 48 − 12 = 36 bits. That makes <b>2<sup>36</sup> ≈ 68.7 billion (64 G) entries</b>. On a 64-bit processor each entry is 8 bytes, so a single flat table would need 2<sup>36</sup> × 8 = 2<sup>39</sup> B = <b>512 GB per process</b>.</p>
<p><b>How to store it:</b> a flat table is far too large to keep, let alone contiguously. <b>Page the page table</b> with a <b>multi-level (hierarchical) page table</b>. x86-64 uses <b>4 levels</b>:</p>
<table style="width:auto"><tr><td>level 4: 9 bits</td><td>level 3: 9 bits</td><td>level 2: 9 bits</td><td>level 1: 9 bits</td><td>offset: 12 bits</td></tr></table>
<p>Each table at each level has 2<sup>9</sup> = 512 entries × 8 B = 4 KB, exactly one page, so tables are paged themselves. <b>Only the tables for parts of the address space actually in use are allocated</b>, which keeps the memory cost small. Alternatives: a <b>hashed page table</b> (good for sparse 64-bit spaces) or an <b>inverted page table</b> (one entry per physical frame). A <b>TLB</b> hides the extra memory accesses.</p>"""

A["peterson"] = """
<p>Pi enters its critical region only when <code>flag[j] == FALSE</code> or <code>turn == i</code>.</p>
<p><b>1. Mutual exclusion.</b> Suppose P0 and P1 were both in their critical regions. Then flag[0] = flag[1] = TRUE, so each must have passed the while because turn equalled its own index. That would require turn == 0 and turn == 1 at the same time, which is impossible. More precisely, turn is a single shared variable holding the value written <b>last</b>. The process that wrote turn last set it to the other process's index, so it must wait while the other is interested. Hence at most one is inside.</p>
<p><b>2. Progress.</b> If Pj is not trying to enter (flag[j] == FALSE, i.e. it is in its remainder region), Pi passes the while at once. If both are trying, turn is either i or j, so exactly one of them passes, and the decision is made in finite time. Only processes in their entry sections take part; a process in its remainder section cannot block anyone.</p>
<p><b>3. Bounded waiting.</b> Suppose Pi is waiting (turn == j and flag[j] == TRUE). When Pj leaves, it sets flag[j] = FALSE, so Pi can enter. If Pj immediately tries again, it sets turn = i, so Pj now waits and Pi enters. Pi therefore waits for at most <b>one</b> entry of Pj into its critical region.</p>"""

A["peterson_bonus"] = """
<p><b>No. Mutual exclusion is violated.</b> In the entry code each process now sets turn to <b>its own</b> index, so a process that has just written turn never waits (its test <code>turn == j</code> is false). Counter-example:</p>
<table><tr><th>Step</th><th>P0</th><th>P1</th></tr>
<tr><td>1</td><td>flag[0] = TRUE; turn = 0</td><td></td></tr>
<tr><td>2</td><td>test turn==1? false → <b>enters CR</b></td><td></td></tr>
<tr><td>3</td><td>(in critical region)</td><td>flag[1] = TRUE; turn = 1</td></tr>
<tr><td>4</td><td>(in critical region)</td><td>test turn==0? false → <b>enters CR</b></td></tr></table>
<p>Both are in the critical region. In general a newly arriving process always gets in, even while the other is inside. (Progress and bounded waiting still hold: a waiting Pi enters as soon as Pj exits, because the exit sets turn = i. But without mutual exclusion the solution is incorrect.)</p>"""

# ----------------------------------------------------------------- questions
HOARE_IMG = '<img src="img/hoare_2022.png" class="scan" alt="Hoare semantics figure from the exam">'
MLQ_BOXES = ('<div class="mlq"><div>system process</div><div>faculty interactive process</div>'
             '<div>student interactive process</div><div>faculty batch process</div><div>student batch process</div></div>')
INTEL_Q = ('<div class="mlq" style="display:flex;gap:4px;align-items:center;justify-content:center">'
           '<span class="box">CPU</span>→<i>logical address</i>→<span class="box">segmentation unit</span>→<i>linear address</i>→'
           '<span class="box">paging unit</span>→<i>physical address</i>→<span class="box">physical memory</span></div>')

BUFFER_CODE = code("""
Producer:
    while (true) {
        /* produce an item in next produced */
        while (((in + 1) % BUFFER_SIZE) == out)
            ; /* do nothing */
        buffer[in] = next_produced;
        in = (in + 1) % BUFFER_SIZE;
    }

Consumer:
    while (true) {
        while (in == out)
            ; /* do nothing */
        next_consumed = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        /* consume the item in next consumed */
    }
""")
FORK_Q = code("""
pid_t pid;

pid = fork();
if (pid == 0) { /* child process */
    fork();
    thread_create( . . .);
}
fork();
""")
PTHREAD_Q = code("""
void *doSomething(void *y) {
    ...
    printf("%d\\n", *y);
    ...
}

int main() {
    pthread_t t1[100];          /* declare a thread */
    int param1, i;

    param1 = 1;
    for (i = 0; i < 100; i++) {
        param1++;
        pthread_create(&(t1[i]), NULL, doSomething, &param1);
    }
    ...
}
""")
PETERSON_Q = code("""
shared int turn;              /* set to i or j */
shared boolean flag[2];       /* set to T or F */

while (TRUE) {
    ...
    flag[i] = TRUE;
    turn = j;
    while (turn == j && flag[j] == TRUE) { /* no-op */ }
    ...
    /* critical region */
    ...
    flag[i] = FALSE;
    ...
    /* remainder region */
    ...
}
""")
PETERSON_BONUS_Q = code("""
shared int turn;              /* set to i or j */
shared boolean flag[2];       /* set to T or F */

while (TRUE) {
    ...
    flag[i] = TRUE;
    turn = i;     /* traditionally set to j */
    while (turn == j && flag[j] == TRUE) { /* no-op */ }
    ...
    /* critical region */
    ...
    flag[i] = FALSE;
    turn = j;     /* not usually done */
    ...
    /* remainder region */
    ...
}
""")
SW_SEM_Q = code("""
Variables
    semaphore mutex;    // (initially = 1)
    semaphore next;     // (initially = 0)
    int next-count = 0;

Each procedure F will be replaced by
    wait(mutex);
        ...
        // body of F;
        ...
    if (next_count > 0)
        signal(next)
    else
        signal(mutex);

For each condition variable x,
    semaphore x_sem;    // (initially = 0)
    int x-count = 0;

The operation x.wait can be implemented as:
    x-count++;
    if (next_count > 0)
        signal(next);
    else
        signal(mutex);
    wait(x_sem);
    x-count--;

The operation x.signal can be implemented as:
    if (x-count > 0) {
        next_count++;
        signal(x_sem);
        wait(next);
        next_count--;
    }
""")

Q_DISABLE = "Explain why implementing synchronization primitives by disabling interrupts is not appropriate in a single-processor system if the synchronization primitives are to be used in user-level programs."
Q_EXEC = "Ordinarily the <code>exec()</code> system call follows the <code>fork()</code>. Explain what would happen if a programmer were to inadvertently place the call to <code>exec()</code> before the call to <code>fork()</code>."
Q_FORKEXEC = "What happens if one thread of a multi-threaded process call <code>fork()</code>? What happens if one thread of a multi-threaded process call <code>exec()</code>?"
Q_AFF = "What is processor affinity? Explain why it needed to be considered during process scheduling on multiple CPU systems."
Q_LOTTERY = "One technique for implementing lottery scheduling works by assigning processes lottery tickets, which are used for allocating CPU time. Whenever a scheduling decision has to be made, a lottery ticket is chosen at random, and the process holding that ticket gets the CPU. The BTV operating system implements lottery scheduling by holding a lottery 50 times each second, with each lottery winner getting 20 milliseconds of CPU time (20 milliseconds × 50 = 1 second). Describe how the BTV scheduler can ensure that higher-priority threads receive more attention from the CPU than lower-priority threads."
Q_REGRESS = "A variation of the round-robin scheduler is the <b>regressive round-robin scheduler</b>. This scheduler assigns each process a time quantum and a priority. The initial value of a time quantum is 50 milliseconds. However, every time a process has been allocated the CPU and uses its entire time quantum (does not block for I/O), 10 milliseconds is added to its time quantum, and its priority level is boosted. (The time quantum for a process can be increased to a maximum of 100 milliseconds.) When a process blocks before using its entire time quantum, its time quantum is reduced by 5 milliseconds, but its priority remains the same. What type of process, namely CPU-bound (such as batch processes) or I/O-bound (such as interactive processes), does the regressive round-robin scheduler favor? Explain."
Q_REGRESS13 = "A variation of the round-robin scheduler is the regressive round-robin scheduler. This scheduler assigns each process a time quantum and a priority. The initial value of a time quantum is 50 milliseconds. However, every time a process has been allocated the CPU and uses its entire time quantum (does not block for I/O), 10 milliseconds is added to its time quantum, and its priority level is boosted. (The time quantum for a process can be increased to a maximum of 100 milliseconds.) When a process blocks before using its entire time quantum, its time quantum is reduced by 5 milliseconds, but its priority remains the same. What type of process (CPU-bound or I/O-bound) does the regressive round-robin scheduler favor? Explain."
Q_FORK = "Consider the following code segment:" + FORK_Q + "a) How many unique processes are created?<br>b) How many unique threads are created?"
Q_PTHREAD = "A student is asked to write a program which will create a hundred POSIX threads. Each thread will print out the value of the parameter passed from <code>main()</code> which are 1, 2, 3, up to 100 respectively. Consider the following code fragment he wrote, please verify its correctness. If incorrect, please correct the error." + PTHREAD_Q
Q_MLQ_LIST = "List two possible scheduling among queues, which we discussed in class."
Q_MLQ_MOD = "Modify the following multilevel queue scheduling system such that a new process will automatically enter the appropriate queue after a few runs." + MLQ_BOXES
Q_CRIT = "Discuss how the following pairs of scheduling criteria conflict in certain settings."
Q_BUSY = "What is <b>busy-waiting</b> in the discussion of critical section problem? Explain how <b>busy-waiting</b> may degrade the system performance."
Q_SEMBLOCK = "How to implement semaphore without <b>busy-waiting</b> using <code>block</code> and <code>wakeup</code>? You need to write down the definition of data structure <code>semaphore</code> and <code>wait</code> and <code>signal</code> operations."
Q_BUFFER = "We have discussed the correct solution to the consumer-producer problem, which does not use any synchronization mechanism, as shown below. Please explain why it can only use <code>BUFFER_SIZE-1</code> elements of buffer." + BUFFER_CODE
Q_RT = "Consider two processes, P<sub>1</sub> and P<sub>2</sub>, where p<sub>1</sub> = d<sub>1</sub> = 50, t<sub>1</sub> = 25, p<sub>2</sub> = d<sub>2</sub> = 75, and t<sub>2</sub> = 30."
Q_RMS = "Can these two processes be scheduled using rate-monotonic scheduling (RMS)? Illustrate your answer using a Gantt chart such as the ones we did in class."
Q_EDF = "Illustrate the scheduling of these two processes using earliest-deadline-first (EDF) scheduling."
Q_HOARE = ("Note that only one process is active within the monitor. Suppose <code>A</code> associated with the condition variable <code>q</code> is resumed when <code>B</code> invokes <code>q.signal()</code>. We discussed two possibile solutions in class. One is <b>signal and wait</b>, and the flow is illustrated in the following (Hoare semantics). Please modify the Hoare semantics and depict the other solution (i.e., <b>signal and continue</b>)." + HOARE_IMG)

CRIT = [("CPU utilization and response time", "c_util_resp"),
        ("Average turnaround time and maximum waiting time", "c_turn_wait"),
        ("I/O device utilization and CPU utilization", "c_io_cpu"),
        ("Deadline and fairness", "c_dead_fair"),
        ("Throughput and context switch overhead", "c_thru_cs")]

def crit_items(prefix, letters=False):
    out = [("q", f"{prefix}", "15 pt", Q_CRIT, None)]
    for k, (t, key) in enumerate(CRIT):
        num = f"{chr(97+k)})" if letters else f"{prefix}.{k+1}"
        out.append(("q", num, "", t, key))
    return out

EXAMS = [
 ("2011", "CS5730 Operating Systems Midterm (2011/11/14)", "", [
  ("h", "1. Short Answer: Your answers should be as concise as possible; aim for three or four sentences."),
  ("q", "1.1", "5 pt", Q_DISABLE, "disable_int"),
  ("q", "1.2", "5 pt", "Provide an example in which multithreading does not provide better performance than a single-threaded solution.", "mt_no_better"),
  ("q", "1.3", "5 pt", "Show that, if the <code>wait()</code> and <code>signal()</code> semaphore operations are not executed atomically, then mutual exclusion may be violated.", "ws_atomic"),
  ("h", "2. Consider a multiprocessor system and a multithreaded program written using the many-to-many threading model. Let the number of user-level threads in the program be more than the number of processors in the system. Discuss the performance implications of the following scenarios."),
  ("q", "2.1", "5 pt", "The number of kernel threads allocated to the program is less than the number of processors.", "m2m_less"),
  ("q", "2.2", "5 pt", "The number of kernel threads allocated to the program is equal to the number of processors.", "m2m_equal"),
  ("q", "2.3", "5 pt", "The number of kernel threads allocated to the program is greater than the number of processors but less than the number of userlevel threads.", "m2m_greater"),
  ("h", "3. Multilevel queue scheduling"),
  ("q", "3.1", "2 pt", Q_MLQ_LIST, "mlq_list"),
  ("q", "3.2", "8 pt", "Describe how Linux support the above two possible inter-queue scheduling.", "linux_mlq"),
  ("h", "4. Consider a logical address space of 64 pages of 1024 words each, mapped onto a physical memory of 32 frames."),
  ("q", "4.1", "5 pt", "How many bits are there in the logical address?", "bits_logical"),
  ("q", "4.2", "5 pt", "How many bits are there in the physical address?", "bits_physical"),
  ("h", "5. A monitor <code>M</code> has processes <code>P1</code> and <code>P2</code> waiting in entry queue and process <code>P3</code> waiting in signal queue. Process <code>P0</code> is active in <code>M</code>. <code>M</code> also has two condition variables <code>x</code>, <code>y</code>. <code>x</code> has processes <code>P4</code> and <code>P5</code> waiting in its corresponding queue, and <code>y</code> has process <code>P6</code> waiting in its corresponding queue. Suppose <code>M</code> implements the signal and wait semantic. List the contents of each queue and the active process after the following events happen. (Note that each event happens right after the above state; that is, these events are independent to each other.)"),
  ("q", "5.1", "5 pt", "New process <code>P7</code> accesses <code>M</code>.", "mon_p7"),
  ("q", "5.2", "5 pt", "<code>P0</code> executes <code>x.signal()</code>.", "mon_xsig"),
  ("q", "5.3", "5 pt", "<code>P0</code> executes <code>y.wait()</code>.", "mon_ywait"),
 ] + crit_items("6", letters=True) + [
  ("q", "7", "20 pt", "Consider the following Peterson's solution for the critical region problem:" + PETERSON_Q + "Prove Peterson's solution satisfy the three required critical region conditions.", "peterson"),
  ("q", "8", "Bonus: 20 pt", "Consider the code below as a variation of Peterson's solution above:" + PETERSON_BONUS_Q + "Does the above solution satisfy the three required critical region conditions? If not, which property or properties is violated?", "peterson_bonus"),
 ]),
 ("2013", "CS5730 Operating Systems Midterm (2013/11/11)", "", [
  ("h", "1. Short Answer: Your answers should be as concise as possible; aim for three or four sentences."),
  ("q", "1.1", "6 pt", Q_DISABLE, "disable_int"),
  ("q", "1.2", "6 pt", "What is busy-waiting in the discussion of critical section problem? Explain how busy-waiting may degrade the system performance, or even deadlock?", "busywait_deadlock"),
  ("q", "1.3", "6 pt", "In class, we discuss the bounded buffer problem which uses two semaphore, empty and full. Explain the usage of these two semaphores.", "bounded_sem"),
  ("q", "1.4", "5 pt", "Illustrate how the two process scheduling criteria, CPU utilization and throughput, may conflict with each other?", "util_thru"),
  ("q", "1.5", "6 pt", Q_FORKEXEC, "fork_exec_mt"),
  ("q", "2", "10 pt", Q_REGRESS13, "regressive"),
  ("q", "3", "10 pt", "Can a multi-threaded solution using multiple user-level threads achieve better performance on a multiprocessor system, which uses the many-to-one threading model, than on a single processor system? Explain.", "m2one_mp"),
  ("h", "4. Multilevel queue scheduling"),
  ("q", "4.1", "4 pt", Q_MLQ_LIST, "mlq_list"),
  ("q", "4.2", "5 pt", "Why is it important for the scheduler to distinguish I/O-bound programs from CPU-bound programs?", "mlq_why"),
  ("q", "4.3", "6 pt", "Modify multilevel queue scheduling so it can distinguish I/O-bound programs from CPU-bound programs.", "mlq_modify3"),
  ("h", "5."),
  ("q", "5.1", "5 pt", "Write to demonstrate how to use the atomic instruction TestAndSet for critical section problem.", "tas"),
  ("q", "5.2", "5 pt", "Illustrate how your solution will fail if TestAndSet is not atomic.", "tas_fail"),
  ("q", "5.3", "5 pt", "Write to demonstrate how to use the atomic instruction Swap for critical section problem.", "swap"),
  ("q", "5.4", "5 pt", "Illustrate how your solution will fail if Swap is not atomic.", "swap_fail"),
  ("q", "6", "10 pt", "Race conditions are possible in many computer systems. Consider a banking system with two methods: <code>deposit(amount)</code> and <code>withdraw(amount)</code>. These two methods are passed the amount that is to be deposited or withdrawn from a bank account. Assume that a husband and wife share a bank account and that concurrently the husband calls the <code>withdraw()</code> method and the wife calls <code>deposit()</code>.<br><i class='note'>(The question stops here on the paper. The textbook version asks: describe how a race condition is possible and what might be done to prevent it.)</i>", "race_bank"),
  ("q", "7", "6 pt", Q_FORK, "forkcount"),
 ]),
 ("2019", "CS5730 Operating Systems Midterm (2019/12/12)", "", [
  ("h", "1. Short Answer: Your answers should be as concise as possible; aim for three or four sentences."),
  ("q", "1.1", "5 pt", Q_EXEC, "exec_before_fork"),
  ("q", "1.2", "5 pt", Q_FORKEXEC, "fork_exec_mt"),
  ("q", "1.3", "5 pt", Q_AFF, "affinity"),
  ("q", "2", "10 pt", Q_LOTTERY, "lottery"),
  ("q", "3", "15 pt", Q_REGRESS, "regressive"),
  ("q", "4", "10 pt", Q_FORK, "forkcount"),
  ("q", "5", "10 pt", Q_HOARE, "hoare_sc"),
  ("q", "6", "20 pt", "In class, we have illustrated the solution for dining-philosopher problem using monitor. However, as I mentioned, the solution is conceptual only since there is no monitor mechanism. We also discussed how to implement a monitor mechanism with <b>signal and wait</b> via semaphores, and thus the dining-philosopher problem solution together with the monitor mechanism with <b>signal and wait</b> via semaphores is a complete solution. Please modify the monitor mechanism with <b>signal and wait</b> via semaphores to <b>signal and continue</b> and integrate them into dining-philosopher problem solution. That is, I would like you to present a complete code for dining-philosopher problem solution which uses a monitor mechanism with <b>signal and continue</b> via semaphores.", "dp_sc"),
  ("h", "7. Multilevel queue scheduling"),
  ("q", "7.1", "5 pt", Q_MLQ_LIST, "mlq_list"),
  ("q", "7.2", "5 pt", Q_MLQ_MOD, "mlq_modify5"),
  ("q", "8", "10 pt", Q_PTHREAD, "pthread"),
 ]),
 ("2020", "CS5730 Operating Systems (2020/12/1; the paper is titled \"Final\")", "Only the photographed pages are available (Q1–Q8).", [
  ("h", "1. Short Answer: Your answers should be as concise as possible; aim for three or four sentences."),
  ("q", "1.1", "5 pt", Q_EXEC, "exec_before_fork"),
  ("q", "1.2", "5 pt", Q_FORKEXEC, "fork_exec_mt"),
  ("q", "1.3", "5 pt", Q_AFF, "affinity"),
  ("q", "2", "10 pt", Q_LOTTERY, "lottery"),
  ("q", "3", "10 pt", Q_REGRESS, "regressive"),
  ("q", "4", "10 pt", Q_FORK, "forkcount"),
 ] + crit_items("5") + [
  ("q", "6", "10 pt", Q_PTHREAD, "pthread"),
  ("h", "7. Consider the Intel address translation scheme shown in the following." + INTEL_Q),
  ("q", "7.1", "10 pt", "Illustrate all the steps that the Intel 80386 takes in translating a logical address into a physical address.", "intel_steps"),
  ("q", "7.2", "5 pt", "What are the advantages to the operating system of hardware that provides such complicated memory translation hardware?", "intel_adv"),
  ("q", "7.3", "5 pt", "Are there any disadvantages to this address-translation system? If so, what are they? If not, why is it not used by every manufacturer?", "intel_disadv"),
  ("q", "8", "10 pt", "Assume we have a demand-paged memory. The page table is held in registers. It takes 8 milliseconds to service a page fault if an empty page is available or the replaced page is not modified, and 20 milliseconds if the replaced page is modified. Memory access time is 100 nanoseconds. Assume that the page to be replaced is modified 70 percent of the time. What is the maximum acceptable page-fault rate for an effective access time of no more than 200 nanoseconds?", "demand_paging"),
 ]),
 ("2021", "CS5730 Operating Systems Midterm (2021/11/30)", "Both 2021 PDFs (\"Operating System Exam_2021\" and \"final-2021f\") contain this same exam.", [
  ("h", "Essay Questions: Your answers should be as concise and clear as possible"),
  ("q", "1", "5 pt", Q_EXEC, "exec_before_fork"),
  ("q", "2", "5 pt", "Why does the socket communication use the port number instead of process id number to identify server or client process?", "socket"),
  ("q", "3", "8 pt", Q_AFF, "affinity"),
  ("q", "4", "7 pt", Q_DISABLE, "disable_int"),
 ] + crit_items("5") + [
  ("h", "6. Multilevel queue scheduling"),
  ("q", "6.1", "5 pt", Q_MLQ_LIST, "mlq_list"),
  ("q", "6.2", "10 pt", Q_MLQ_MOD, "mlq_modify5"),
  ("h", "7. Multilevel queue scheduling <span class='note'>(heading as printed; the questions are about synchronization)</span>"),
  ("q", "7.1", "5 pt", Q_BUSY, "busywait"),
  ("q", "7.2", "10 pt", Q_SEMBLOCK, "sem_block"),
  ("q", "8", "10 pt", Q_BUFFER, "buffer_n1"),
  ("h", "9. " + Q_RT),
  ("q", "9.1", "10 pt", Q_RMS, "rms"),
  ("q", "9.2", "10 pt", Q_EDF, "edf"),
 ]),
 ("2022", "CS5730 Operating Systems Midterm (2022/11/22)", "", [
  ("h", "Essay Questions: Your answers should be as concise and clear as possible"),
  ("q", "1", "5 pt", Q_DISABLE, "disable_int"),
  ("q", "2", "15 pt", Q_HOARE, "hoare_sc"),
  ("q", "3", "20 pt", "In class, we have discussed implementing monitor with <b>signal and wait</b> via semaphores as follows." + SW_SEM_Q + "Please modify the above code to implement <b>signal and continue</b>.", "sc_sem"),
  ("q", "4", "10 pt", "Suppose a architecture use 48-bit addressing with 4K paging on 64-processors. How much memory space a process may have? How many entries a page table may have? How should a page table be stored in memory?", "paging48"),
  ("h", "5. Multilevel queue scheduling"),
  ("q", "5.1", "5 pt", Q_MLQ_LIST, "mlq_list"),
  ("q", "5.2", "5 pt", Q_MLQ_MOD, "mlq_modify5"),
  ("h", "6. Multilevel queue scheduling <span class='note'>(heading as printed)</span>"),
  ("q", "6.1", "5 pt", Q_BUSY, "busywait"),
  ("q", "6.2", "5 pt", Q_SEMBLOCK, "sem_block"),
  ("q", "7", "10 pt", Q_BUFFER, "buffer_n1"),
  ("h", "8. " + Q_RT),
  ("q", "8.1", "10 pt", Q_RMS, "rms"),
  ("q", "8.2", "10 pt", Q_EDF, "edf"),
 ]),
]

CSS = """
:root{ --acc:#0b4f8a; --rule:#bbb; --box:#f3f5f8; --qbg:#f6f7f9; }
@page{ size: Letter; margin: 0.55in 0.6in; }
*{ box-sizing:border-box; }
html,body{ background:#fff; color:#111; }
body{ font: 10pt/1.38 "Helvetica Neue", Arial, sans-serif; margin:0; padding:16px; max-width:8in; }
@media print{ body{ padding:0; max-width:none; } }
h1{ font-size:17pt; margin:0 0 4px; }
.lead{ color:#444; margin-bottom:10px; }
.toc td{ padding:2px 8px; }
.exam{ break-before:page; }
.exam h2{ font-size:14pt; color:#fff; background:var(--acc); padding:5px 8px; margin:0 0 4px; }
.exam .meta{ font-size:9pt; color:#555; margin-bottom:8px; }
.hdr{ font-weight:bold; margin:12px 0 4px; padding:4px 8px; border-left:4px solid var(--acc); background:var(--qbg); break-after:avoid; }
.item{ margin:8px 0 12px; }
.qbox{ background:var(--qbg); border:1px solid #d6dbe2; border-left:4px solid var(--acc); padding:6px 9px; break-inside:avoid; break-after:avoid; }
.qnum{ font-weight:bold; color:var(--acc); margin-right:4px; }
.pts{ font-size:8.5pt; color:#555; }
.yr{ float:right; font-size:8pt; color:#fff; background:#555; padding:0 5px; border-radius:2px; }
.ans{ padding:4px 2px 0 12px; border-left:2px solid #cfe0f2; margin-left:2px; }
.ans .lbl{ font-weight:bold; color:#0a6b2d; font-size:9pt; letter-spacing:.03em; }
p{ margin:3px 0 5px; } ul,ol{ margin:3px 0 5px; padding-left:20px; } li{ margin:1px 0 2px; }
pre{ font: 8.4pt/1.3 "DejaVu Sans Mono", Menlo, Consolas, monospace; background:var(--box); border:1px solid #dde; padding:5px 7px; margin:4px 0 6px; white-space:pre-wrap; }
code{ font: 8.8pt "DejaVu Sans Mono", Menlo, Consolas, monospace; background:var(--box); padding:0 2px; }
.qbox pre{ background:#fff; }
table{ border-collapse:collapse; margin:4px 0 6px; font-size:9pt; break-inside:avoid; }
th,td{ border:1px solid var(--rule); padding:2px 6px; text-align:left; vertical-align:top; }
th{ background:var(--box); }
.gantt{ display:flex; width:100%; margin:6px 0 0; border:1px solid #333; font-size:8.5pt; break-inside:avoid; }
.gantt div{ border-right:1px solid #333; text-align:center; padding:3px 0; overflow:hidden; white-space:nowrap; }
.gantt div:last-child{ border-right:0; }
.g1{ background:#cfe3ff; } .g2{ background:#ffd9b3; } .gi{ background:#eee; color:#777; } .gx{ background:#ffb3b3; }
.ticks{ display:flex; width:100%; font-size:8pt; color:#444; margin-bottom:6px; }
.ticks span{ white-space:nowrap; }
.fig{ display:block; margin:6px auto; max-width:100%; height:auto; break-inside:avoid; }
.scan{ display:block; width:70%; margin:6px auto 2px; border:1px solid #ccc; }
.mlq{ margin:6px auto; width:60%; text-align:center; font-size:9pt; }
.mlq div{ border:1px solid #888; margin:3px 0; padding:2px; background:#fff; }
.mlq .box{ border:1px solid #888; padding:2px 5px; background:#fff; }
.note{ color:#555; font-size:9pt; }
"""


COMPACT_CSS = """
@page{ size: Letter; margin: 0.38in 0.42in; }
body{ font-size:8.6pt; line-height:1.27; }
h1{ font-size:12pt; margin:0 0 2px; }
.lead, .toc{ display:none; }
.exam{ break-before:auto; }
.exam ~ .exam{ break-before:page; }
.exam h2{ font-size:10.5pt; padding:2px 6px; margin:0 0 2px; }
.hdr{ margin:5px 0 2px; padding:2px 6px; }
.item{ margin:4px 0 6px; }
.qbox{ padding:3px 6px; }
.ans{ padding:2px 0 0 8px; }
p{ margin:1px 0 3px; } ul,ol{ margin:1px 0 3px; padding-left:16px; } li{ margin:0 0 1px; }
pre{ font-size:7.1pt; line-height:1.17; padding:3px 5px; margin:2px 0 3px; }
code{ font-size:7.6pt; }
table{ font-size:7.8pt; margin:2px 0 3px; } th,td{ padding:1px 4px; }
.fig{ max-height:2.3in; width:auto; margin:3px auto; }
.scan{ width:52%; margin:3px auto 1px; }
.mlq{ width:48%; margin:3px auto; font-size:7.8pt; } .mlq div{ margin:1px 0; padding:1px; }
.gantt{ font-size:7.5pt; margin-top:3px; } .gantt div{ padding:1px 0; }
.note{ font-size:7.8pt; }
pre.long{ column-count:2; column-gap:12px; column-rule:1px solid #dde; font-size:6.9pt; }
"""

def wc(h):
    import re
    t = re.sub(r"<pre>.*?</pre>|<svg.*?</svg>|<table.*?</table>", " ", h, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return len(t.split())

def build(years=None, compact=False):
    exams = [e for e in EXAMS if not years or e[0] in years]
    out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
           f"<title>Past Exam Solutions</title><style>{CSS}{COMPACT_CSS if compact else ''}</style></head><body>"]
    out.append("<h1>CS5730 Operating Systems: " + (f"{exams[0][0]} Midterm Solutions" if years else "Past Exam Solutions") + "</h1>")
    out.append("<p class='lead'>All past papers in the repo (2011, 2013, 2019, 2020, 2021, 2022), in order. Each entry gives the year, "
               "the full question as printed, then a model answer sized to fit the space on the exam paper (prose kept to about 250 words; "
               "code, tables and diagrams added where the question needs them). Repeated questions use the same answer every time.</p>")
    out.append("<table class='toc'><tr><th>Year</th><th>Paper</th><th>Questions</th></tr>")
    for yr, title, note, items in exams:
        n = sum(1 for it in items if it[0] == "q" and it[4])
        out.append(f"<tr><td>{yr}</td><td>{title}</td><td>{n} answers</td></tr>")
    out.append("</table>")
    long = []
    for yr, title, note, items in exams:
        out.append(f"<section class='exam'><h2>{yr} · {title}</h2>")
        if note:
            out.append(f"<div class='meta'>{note}</div>")
        for it in items:
            if it[0] == "h":
                out.append(f"<div class='hdr'>{it[1]}</div>")
                continue
            _, num, pts, qtext, key = it
            pts_html = f" <span class='pts'>({pts})</span>" if pts else ""
            out.append("<div class='item'>")
            out.append(f"<div class='qbox'><span class='yr'>{yr}</span><span class='qnum'>Q{num}</span>{pts_html} {qtext}</div>")
            if key:
                out.append(f"<div class='ans'><span class='lbl'>ANSWER</span>{A[key]}</div>")
                if wc(A[key]) > 300:
                    long.append((yr, num, wc(A[key])))
            out.append("</div>")
        out.append("</section>")
    out.append("</body></html>")
    return "".join(out), long

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    import sys
    # usage: build_solutions.py            -> past_exam_solutions.html (all years)
    #        build_solutions.py 2022       -> solutions_2022.html (one paper)
    #        add --compact for a dense print layout (e.g. 2022 fits 4 pages)
    compact = "--compact" in sys.argv
    years = [a for a in sys.argv[1:] if a != "--compact"]
    page, long = build(years, compact)
    name = f"solutions_{'_'.join(years)}.html" if years else "past_exam_solutions.html"
    if compact:
        name = name.replace(".html", "_compact.html")
    if years:
        page = page.replace("<p class='lead'>All past papers in the repo (2011, 2013, 2019, 2020, 2021, 2022), in order.",
                            "<p class='lead'>The " + ", ".join(years) + " paper only, in order.")
    with open(os.path.join(here, name), "w") as f:
        f.write(page)
    print(name, "| prose > 300 words:", long or "none")
