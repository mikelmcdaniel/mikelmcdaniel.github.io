import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # N-M Balancers

    I recently came across a challenge, inspired by the 2020 game Factorio, someone posted on the internet. Here's a little description of the problem and the (partial) solution I came up with. If it sounds fun, I highly recommend trying out the problem for yourself!

    An N-M balancer is something that has N inputs and M outputs. Whatever goes into 1 input is evenly balanced among the M outputs. What's the minimum number of 2-2 balancers needed to make an N-M balancer?

    For reference, here's an example of a 2-4 balancer:
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import altair as alt

    return alt, mo


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid("""
    graph LR
        n0("2-2 balancer")
        n2("2-2 balancer")
        n3("2-2 balancer")
        inputs --> n0
        inputs --> n0
        n0 --> n2
        n0 --> n3
        n2 --> outputs
        n2 --> outputs
        n3 --> outputs
        n3 --> outputs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here's an example of a 1-3 balancer:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid("""
    graph LR
        n0("2-2 balancer")
        n2("2-2 balancer")
        n3("2-2 balancer")
        inputs --> n0
        n0 --> n2
        n0 --> n3
        n2 --> outputs
        n2 --> outputs
        n3 --> outputs
        n3 -- backwards edge --> n0
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Initial Approach: Brute Force

    My intitial thought was to brute-force it: generate all matrix representations of graphs where the 2-2 balancer nodes have at most 2 inputs and outputs. For example, a 2-2 balancer can be represented as $\begin{pmatrix} \frac{1}{2} & \frac{1}{2} \\ \frac{1}{2} & \frac{1}{2} \end{pmatrix}$ where each row represents an input and each column represents an output.

    However! The representation I actually used is redundant with 1 row/column for each input, 1 row/colum for each output, and 1 row/column for each 2-2 balancer. So the 2-2 balancer would be represented as

    $\begin{pmatrix} 0 & 0 & 1 & 0  & 0 \\ 0 & 0 & 1 & 0  & 0 \\ 0 & 0 & 0 & \frac{1}{2} & \frac{1}{2} \\ 0 & 0 & 0 & 1  & 0 \\ 0 & 0 & 0 & 0 & 1  \end{pmatrix}$

    Looking at each row, we see the first input (row number 0) takes all of its inputs and redirects it to the 2-2 balancer (row 2) which then redirects half of it's input to each output (the last rows: rows 3 and 4).

    The 1-3 balancer graph above would be represented with this matrix (with 1+3+3 rows/columns):

    $G = \begin{pmatrix} 0 & 1 & 0 & 0 & 0 & 0 & 0  \\ 0 & 0 & \frac{1}{2} & \frac{1}{2} & 0 & 0 & 0  \\ 0 & 0 & 0 & 0 & \frac{1}{2} & \frac{1}{2} & 0  \\ 0 & \frac{1}{2} & 0 & 0 & 0 & 0 & \frac{1}{2} \\ 0 & 0 & 0 & 0 & 1 & 0 & 0  \\ 0 & 0 & 0 & 0 & 0 & 1 & 0  \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 \end{pmatrix}$

    Each row of the matrix tells you where anything on that input/node/output will go in 1 step. If you multiply the matrix by itself once, then each row tells you where anything on that input/node/output will go in 2 steps. By exponentiating the matrix with itself $K$ times, you can see where the things go in 1, 2, 4, 8, 16, ..., $2^K$ steps.
    """)
    return


@app.cell(hide_code=True)
def _():
    import collections
    import copy
    from dataclasses import dataclass, field
    import functools
    import heapq
    import itertools
    import math
    import time

    import numpy as np
    import pandas as pd

    return collections, copy, dataclass, field, heapq, itertools, math, np, pd


@app.cell
def _(mo, np):
    def _num_to_latex(x):
        if int(x) == x:
            return str(int(x))
        return str(round(x, 4))

    def _mat_to_latex(mat):
        mid = r" \\ ".join(" & ".join(map(_num_to_latex, row)) for row in mat)
        return f"\\begin{{pmatrix}} {mid} \\end{{pmatrix}}"

    def _():
        from fractions import Fraction
        md = []
        g = np.array([
            [0. , 1. , 0. , 0. , 0. , 0. , 0. ],
            [0. , 0. , 0.5, 0.5, 0. , 0. , 0. ],
            [0. , 0. , 0. , 0. , 0.5, 0.5, 0. ],
            [0. , 0.5, 0. , 0. , 0. , 0. , 0.5],
            [0. , 0. , 0. , 0. , 1. , 0. , 0. ],
            [0. , 0. , 0. , 0. , 0. , 1. , 0. ],
            [0. , 0. , 0. , 0. , 0. , 0. , 1. ]])
        m = ""
        g @= g
        for k in range(1, 4):
            g @= g
            md.append(f"$G^{{{2**(k - 1)}}} \\times G^{{{2**(k - 1)}}} = G^{{{2**k}}} \\approx")
            md.append(_mat_to_latex(g))
            md.append("$\n\n")
        return "".join(md)



    mo.md(_())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looking at $G^{2^k}$, we can see that anything that goes to the first (and only input at row 0), gets evenly distributed to the 3 outputs (last 3 columns).

    The strategy of matrix exponentiation is a little fraught because there's always a small amount that isn't sent to any of the 3 outputs after $2^k$ steps but it's small enough that I think it's safe to just choose a large $k$.

    The real issue with this approach is the number of matrices we have to check. Even for a relatively small number of 2-2 balancers, e.g. 10, we would need to generate all matrices with 10x10 matrices where each row/column has 1 or 2 non-zero entries.
    """)
    return


@app.cell
def _(math):
    import sys


    sys.setrecursionlimit(999_999)


    MWMS_CACHE = {}
    MAX_CELL_VALUE = 1
    def matrices_with_max_sums(
            col_max_sums: tuple[int, ...],
            row_max_sums: tuple[int, ...],
            col: int=0) -> int:
        if not row_max_sums or not col_max_sums:
            return 1
        if col >= len(col_max_sums) or not row_max_sums[0]:
            return matrices_with_max_sums(col_max_sums, row_max_sums[1:], 0)

        while not col_max_sums[col]:
            col_max_sums = col_max_sums[:col] + col_max_sums[col + 1:]
            if col >= len(col_max_sums):
                return matrices_with_max_sums(col_max_sums, row_max_sums[1:], 0)
        col_max_sums = tuple(sorted(col_max_sums[:col])) + (col_max_sums[col],) + tuple(sorted(col_max_sums[col + 1:]))
        if col == 0:
            row_max_sums = tuple(sorted(row_max_sums))
            if len(row_max_sums) < len(col_max_sums):
                row_max_sums, col_max_sums = col_max_sums, row_max_sums

        cache_key = (col_max_sums, row_max_sums, col)
        if not cache_key in MWMS_CACHE:
            MWMS_CACHE[cache_key] = sum(
                matrices_with_max_sums(
                    col_max_sums[:col] + (col_max_sums[col] - delta,) + col_max_sums[col + 1:],
                    (row_max_sums[0] - delta,) + row_max_sums[1:],
                    col + 1)
                for delta in range(min(col_max_sums[col], row_max_sums[0], MAX_CELL_VALUE) + 1)
            )
        return MWMS_CACHE[cache_key]


    def _table_md():
        table = []
        table.append("N | lower bound number of NxN graphs where nodes have <= 2 incoming or outgoing edges | upper bound")
        table.append("--|-----------------------------------------------------------------------------------|-------------")
        for n in list(range(1, 16)) + [30]:
            # Note: Dividing by n! is meant to account for reordering nodes in the graph *but* that will
            # discount some graphs that are unique, such as graphs where 2 nodes have identical connections.
            upper_bound = matrices_with_max_sums(tuple([2]*n), tuple([2]*n))
            lower_bound = upper_bound // math.factorial(n)
            table.append(f"{n} | {lower_bound} ({math.ceil(math.log10(lower_bound))} digits) | {upper_bound}")
        return print("\n".join(table))

    _table_md()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So... maybe 633,055,041 isn't so many 10-node graphs if we don't need to calculate a number closer to the upper bound of 2,297,230,134,084,416.

    However 171,583,167,860 is definitely too much for 12-node graphs and there are probably many many times more than that. So this might be a workable strategy for small graphs but not for large ones. The lower bound appears to grow super-exponentially.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Next Approach: Composition

    What if we strictly build N-M balancers out of smaller balancers? We might not find the minimal graphs for building N-M balancers out of 2-2 balancers but we should be able to get relatively small balancers.

    As far as I can tell there are three ways to make a new balancer out of existing balances.

    ### 1. Ignore an input

    If you simply ignore an input, then an N-M balancer becomes an (N-1)-M balancer.

    ### 2. Feed an output into an input

    If you take one of the outputs and put it back as an input, then an N-M balancer becomes a (N-1)-(M-1) balancer.

    ### 3. Multiplex

    Start with X copies of an A-B balancer and B copies of an X-Y balancer. Then take each output from each A-B balancer and feed it to a different X-Y balancer. Now you have an AX-BY balancer.

    For example, below we take 2 1-3 balancers and feed them into 3 2-3 balancers to create 2-9 balancer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid("""graph LR
        n0("1-3")
        n1("1-3")
        n2("2-3")
        n3("2-3")
        n4("2-3")
        n0 --> n2
        n0 --> n3
        n0 --> n4
        n1 --> n2
        n1 --> n3
        n1 --> n4
        n2 --> outputs
        n2 --> outputs
        n2 --> outputs
        n3 --> outputs
        n3 --> outputs
        n3 --> outputs
        n4 --> outputs
        n4 --> outputs
        n4 --> outputs
        inputs --> n0
        inputs --> n1
        """)
    return


@app.cell(hide_code=True)
def _(collections, copy, dataclass, field, itertools):
    # Balancer Graph

    BALANCER_INPUTS = -1
    BALANCER_OUTPUTS = -2

    assert BALANCER_INPUTS < 0
    assert BALANCER_OUTPUTS < 0

    def _mermaid_node_name(n: int) -> str:
        if n == BALANCER_INPUTS:
            return "inputs"
        if n == BALANCER_OUTPUTS:
            return "outputs"
        return f'n{n}'

    def _mermaid_node_label(n: int) -> str:
        if n == BALANCER_INPUTS:
            return "inputs"
        if n == BALANCER_OUTPUTS:
            return "outputs"
        return f'{n}'

    @dataclass
    class BalancerGraph:
        # edges[x][y] == number_edges_from_x_to_y
        edges: dict[int, dict[int, int]] = field(default_factory=lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
        # inv_edges[y][x] == number_edges_from_x_to_y
        inv_edges: dict[int, dict[int, int]] = field(default_factory=lambda: collections.defaultdict(lambda: collections.defaultdict(int)))

        def add_node(self, x):
            self.edges[x]
            self.inv_edges[x]

        def add_edge(self, src, dst, count=1):
            self.add_node(src)
            self.add_node(dst)
            self.edges[src][dst] += count
            self.inv_edges[dst][src] += count

        def remove_edge(self, src, dst, count=1):
            # assert src in self.edges
            # assert dst in self.inv_edges
            self.edges[src][dst] -= count
            if not self.edges[src][dst]:
                del self.edges[src][dst]
            else:
                assert self.edges[src][dst] > 0
            self.inv_edges[dst][src] -= count
            if not self.inv_edges[dst][src]:
                del self.inv_edges[dst][src]
            else:
                assert self.inv_edges[dst][src] > 0

        def copy(self, min_node_id: int | None=None) -> "BalancerGraph":
            if min_node_id is None or min(self.edges) == min_node_id:
                return copy.deepcopy(self)
            g = BalancerGraph()
            nodes = {
                cur: new
                for new, cur in
                zip(itertools.count(min_node_id), sorted(e for e in self.edges if e >= 0))}
            nodes[BALANCER_OUTPUTS] = BALANCER_OUTPUTS
            nodes[BALANCER_INPUTS] = BALANCER_INPUTS
            for src, dsts in sorted(self.edges.items()):
                new_src = nodes[src]
                for dst, count in sorted(dsts.items()):
                    new_dst = nodes[dst]
                    g.add_edge(new_src, new_dst, count)
            return g

        def num_internal_nodes(self) -> int:
            return len(self.edges) - 2  # Don't count INPUTS/OUTPUTS

        def nodes(self):
            return iter(self.edges)

        def sorted_internal_nodes(self) -> list[int]:
            return sorted(self.nodes())[2:]  # Don't count INPUTS/OUTPUTS

        def num_inputs(self) -> int:
            return sum(self.edges[BALANCER_INPUTS].values())

        def num_outputs(self) -> int:
            return sum(self.inv_edges[BALANCER_OUTPUTS].values())

        def mermaid_str(self) -> str:
            m = ["graph LR"]
            for node in self.sorted_internal_nodes():
                m.append(f'{_mermaid_node_name(node)}("{_mermaid_node_label(node)}")')
            for src, dsts in self.edges.items():
                src_name = _mermaid_node_name(src)
                for dst, count in dsts.items():
                    dst_name = _mermaid_node_name(dst)
                    for _ in range(count):
                        m.append(f"{src_name} --> {dst_name}")
            return "    \n".join(m)


    def balancer_2_2() -> BalancerGraph:
        g = BalancerGraph()
        g.add_edge(BALANCER_INPUTS, 0, 2)
        g.add_edge(0, BALANCER_OUTPUTS, 2)
        return g

    def infeed_one(g: BalancerGraph) -> BalancerGraph:
        g = g.copy()
        # assert g.inv_edges[BALANCER_OUTPUTS]
        # assert g.edges[BALANCER_INPUTS]
        out_node = max(g.inv_edges[BALANCER_OUTPUTS])
        in_node = max(g.edges[BALANCER_INPUTS])
        g.remove_edge(out_node, BALANCER_OUTPUTS)
        g.remove_edge(BALANCER_INPUTS, in_node)
        g.add_edge(out_node, in_node)
        return g

    def ignore_one_input(g: BalancerGraph) -> BalancerGraph:
        g = g.copy()
        # assert g.edges[BALANCER_INPUTS]
        in_node = max(g.edges[BALANCER_INPUTS])
        g.remove_edge(BALANCER_INPUTS, in_node)
        return g

    def multiplex(in_g: BalancerGraph, out_g: BalancerGraph, num_in_copies=None, num_out_copies=None) -> BalancerGraph:
        if num_in_copies is None:
            num_in_copies = out_g.num_inputs()
        if num_out_copies is None:
            num_out_copies = in_g.num_outputs()
        # print(f"{num_in_copies=}  {num_out_copies=}")
        in_gs = [in_g.copy(i * in_g.num_internal_nodes()) for i in range(num_in_copies)]
        num_ing_nodes = num_in_copies * in_g.num_internal_nodes()
        out_gs = [out_g.copy(num_ing_nodes + i * out_g.num_internal_nodes()) for i in range(num_out_copies)]
        g = BalancerGraph()
        for ig in in_gs:
            for og in out_gs:
                ig_to_og_node = min(ig.inv_edges[BALANCER_OUTPUTS])
                og_from_ig_node = min(og.edges[BALANCER_INPUTS])
                ig.remove_edge(ig_to_og_node, BALANCER_OUTPUTS)
                og.remove_edge(BALANCER_INPUTS, og_from_ig_node)
                g.add_edge(ig_to_og_node, og_from_ig_node)
        for ig in in_gs:
            for n, c in list(ig.inv_edges[BALANCER_OUTPUTS].items()):
                ig.remove_edge(n, BALANCER_OUTPUTS, c)
        for og in out_gs:
            for n, c in list(og.edges[BALANCER_INPUTS].items()):
                og.remove_edge(BALANCER_INPUTS, n, c)
        for sub_g in itertools.chain(in_gs, out_gs):
            for src, dsts in sub_g.edges.items():
                for dst, count in dsts.items():
                    g.add_edge(src, dst, count)
        return g

    return (
        BALANCER_INPUTS,
        BALANCER_OUTPUTS,
        BalancerGraph,
        balancer_2_2,
        ignore_one_input,
        infeed_one,
        multiplex,
    )


@app.cell(hide_code=True)
def _(dataclass):
    @dataclass(frozen=True, order=True)
    class Balancer22Inst:
        pass

    @dataclass(frozen=True, order=True)
    class InfeedOneInst:
        n: int
        m: int

    @dataclass(frozen=True, order=True)
    class IgnoreOneInputInst:
        n: int
        m: int

    @dataclass(frozen=True, order=True)
    class MultiplexInst:
        in_n: int
        in_m: int
        out_n: int
        out_m: int
        num_in_copies: int
        num_out_copies: int


    return Balancer22Inst, IgnoreOneInputInst, InfeedOneInst, MultiplexInst


@app.cell(hide_code=True)
def _(mo):
    MAX_NODES = mo.ui.number(start=1, step=1, value=1000, label="Maximum Nodes (all balancer with more nodes will be ignored)")
    MAX_NODES
    return (MAX_NODES,)


@app.cell(hide_code=True)
def _(
    Balancer22Inst,
    IgnoreOneInputInst,
    InfeedOneInst,
    MAX_NODES,
    MultiplexInst,
    collections,
    heapq,
    mo,
):
    def get_balancer_min_nodes(max_nodes):
        """Generate 2 tables: balancer_min_nodes, graph_instructions

        balancer_min_nodes[n, m] == minumum number of nodes needed for a balancer with n inputs and m outputs
        graph_instructions[n, m] == "instructions" for how to construct a graph for an n-m balancer

        for example:
            balancer_min_nodes[2, 2] == 1
            graph_instructions[2, 2] = Balancer22Inst()

            balancer_min_nodes[1, 2] == 1
            graph_instructions[1, 2] = IgnoreOneInputInst(2, 2)
        """
        def push(r, n, m, g):
            if n < 1 or m < 1 or r > max_nodes:
                return
            if (n, m) in balancer_min_nodes:
                # assert balancer_min_nodes[n, m] <= r
                return
            heapq.heappush(q, (r, n, m, g))

        # balancer_max_nodes = {} # Not the true "max"... just the most min can be (as far as we know)
        n2r2m = collections.defaultdict(lambda: collections.defaultdict(list))
        m2r2n = collections.defaultdict(lambda: collections.defaultdict(list))
        balancer_min_nodes = {}
        graph_instructions = {}
        q = [(1, 2, 2, Balancer22Inst())]
        last_progress_update = 0
        with mo.status.progress_bar(total=max_nodes**2, show_rate=False) as progress_bar:
            while q:
                r, n, m, g = heapq.heappop(q)
                if (n, m) in balancer_min_nodes:
                    # assert balancer_min_nodes[n, m] <= r
                    continue
                # balancer_max_nodes[n, m] = r
                balancer_min_nodes[n, m] = r
                graph_instructions[n, m] = g
                n2r2m[n][r].append(m)
                m2r2n[m][r].append(n)
  
                if r > last_progress_update:
                    # There are on the order of r (n,m) pairs where r is the minimum number of nodes
                    # So we estimate progress this way... Just a very rough approximation.
                    progress_bar.update(r**2 - last_progress_update**2)
                    last_progress_update = r

                # f(n, m) <= f(n - 1, m - 1)
                push(r, n - 1, m - 1, InfeedOneInst(n, m))
                # f(n, m) <= f(n - 1, m)
                push(r, n - 1, m, IgnoreOneInputInst(n, m))

                # f(n, m) <= kn * f(n_div_kn, km) + km * f(kn, m_div_km) where kn divides n and km divides m
                # f(a * x, b * y) <= x * f(a, b) + b * f(x, y)
                # a = n, b = m, f(a, b) = r
                for x, r2m in n2r2m.items():
                    for f_xy in range(1, (max_nodes - x * r) // m + 1):
                        for y in r2m[f_xy]:
                            push(x * r + m * f_xy, n * x, m * y, MultiplexInst(n, m, x, y, x, m))
                # del x, y, f_xy, new_r
                for b, r2n in m2r2n.items():
                    for f_ab in range(1, (max_nodes - b * r) // n):
                        for a in r2n[f_ab]:
                            push(n * f_ab + b * r, a * n, b * m, MultiplexInst(a, b, n, m, n, b))
                # del a, b, f_ab, new_r
        return balancer_min_nodes, graph_instructions

    balancer_min_nodes, graph_instructions = get_balancer_min_nodes(max_nodes=MAX_NODES.value)
    return balancer_min_nodes, graph_instructions


@app.cell(hide_code=True)
def _(BALANCER_INPUTS, BALANCER_OUTPUTS, BalancerGraph, dataclass, field, np):
    def row_normalize_matrix(m) -> None:
        for row_index in range(len(m)):
            row = m[row_index, :]
            if row.sum():
                row /= row.sum()

    @dataclass
    class _NodeIdAssigner:
        # Convert g to a matrix where each input is one of the first rows/columns
        # and every output is in one of the last rows/columns
        input_ids_by_dst: dict[int, slice] = field(default_factory=dict)
        next_input_id: int = 0
        output_ids_by_src: dict[int, slice] = field(default_factory=dict)
        next_output_id: int = 0

        def get(self, src, dst, count):
            if src == BALANCER_INPUTS:
                # assert dst != BALANCER_OUTPUTS
                if dst not in self.input_ids_by_dst:
                    self.input_ids_by_dst[dst] = slice(
                        self.next_input_id,
                        self.next_input_id + count)
                    self.next_input_id += count
                return self.input_ids_by_dst[dst], (dst,)
            elif dst == BALANCER_OUTPUTS:
                # assert src != BALANCER_INPUTS
                if src not in self.output_ids_by_src:
                    self.output_ids_by_src[src] = slice(
                        self.next_output_id,
                        self.next_output_id + count)
                    self.next_output_id += count
                return src, self.output_ids_by_src[src]
            else:
                return src, dst


    def graph_to_matrix(g: BalancerGraph):
        g = g.copy(min_node_id=g.num_inputs())
        num_inputs = g.num_inputs()
        outputs_offset = num_inputs + g.num_internal_nodes()
        node_ids = _NodeIdAssigner(next_output_id=outputs_offset)
        num_nodes = outputs_offset + g.num_outputs()
        m = np.zeros((num_nodes, num_nodes))
        # assert not g.edges.get(BALANCER_OUTPUTS)
        # assert not g.inv_edges.get(BALANCER_INPUTS)
        for src, dsts in g.edges.items():
            for dst, count in dsts.items():
                m[node_ids.get(src, dst, count)] = count
        # make each output go to itself
        m[outputs_offset:, outputs_offset:] = np.identity(num_nodes - outputs_offset)
        row_normalize_matrix(m)
        return m


    return (graph_to_matrix,)


@app.cell(hide_code=True)
def _(
    Balancer22Inst,
    IgnoreOneInputInst,
    InfeedOneInst,
    MultiplexInst,
    balancer_2_2,
    graph_instructions,
    ignore_one_input,
    infeed_one,
    itertools,
    multiplex,
):
    def graph_for_nm(n: int, m: int) -> str:
        i = graph_instructions[n, m]
        if isinstance(i, MultiplexInst):
            in_g = graph_for_nm(i.in_n, i.in_m)
            out_g = graph_for_nm(i.out_n, i.out_m)
            return multiplex(in_g, out_g, i.num_in_copies, i.num_out_copies)
        elif isinstance(i, InfeedOneInst):
            return infeed_one(graph_for_nm(i.n, i.m))
        elif isinstance(i, IgnoreOneInputInst):
            return ignore_one_input(graph_for_nm(i.n, i.m))
        elif isinstance(i, Balancer22Inst):
            return balancer_2_2()
        raise ValueError(repr(i))

    def _mermaid_multiply(n, name, diagram):
        return name, diagram
        # if n <= 1:
        #     return name, diagram
        # return f"{name}_{n}", f'subgraph {name}_{n}["{n} times"]\n  {name}\nend\n'

    def _mermaid_for_nm(n: int, m: int, name_generator) -> str:
        i = graph_instructions[n, m]
        name = next(name_generator)
        if isinstance(i, MultiplexInst):
            in_name, in_diagram = _mermaid_multiply(i.num_in_copies, *_mermaid_for_nm(i.in_n, i.in_m, name_generator))
            out_name, out_diagram = _mermaid_multiply(i.num_out_copies, *_mermaid_for_nm(i.out_n, i.out_m, name_generator))
            parts = [f'  subgraph {name}["{n}-{m} multiplex"]\n']
            inner_input_name = next(name_generator)
            for sub_name in (in_name, out_name):
                parts.append(f"    {sub_name}\n")
            parts.append(f"    {inner_input_name}((input))\n")
            parts.append("end\n")
            for sub_diagram in (in_diagram, out_diagram):
                parts.append(f"    {sub_diagram}\n")
            parts.append(f"{inner_input_name} -- {i.num_in_copies} --> {in_name}\n")
            parts.append(f"{in_name} -- {i.num_out_copies} --> {out_name}\n")
            # parts.append(f"{in_name} --> {out_name}\n")
            return name, "".join(parts)
        elif isinstance(i, InfeedOneInst):
            sub_name, sub_diagram = _mermaid_for_nm(i.n, i.m, name_generator)
            return name, f'  subgraph {name}["{n}-{m} infeed_one"]\n    {sub_name}\n  end\n{sub_diagram}\n'
        elif isinstance(i, IgnoreOneInputInst):
            sub_name, sub_diagram = _mermaid_for_nm(i.n, i.m, name_generator)
            return name, f'  subgraph {name}["{n}-{m} ignore_one_input"]\n    {sub_name}\n  end\n{sub_diagram}\n'
        elif isinstance(i, Balancer22Inst):
            return name, f'  {name}("{n}-{m}")\n'
        raise ValueError(repr(i))

    def mermaid_for_nm(n: int, m: int) -> str:
        _, diagram_body = _mermaid_for_nm(n, m, name_generator=(f"x{i}" for i in itertools.count()))
        return "graph\n" + diagram_body


    def repr_for_nm(n: int, m: int) -> str:
        i = graph_instructions[n, m]
        if isinstance(i, Balancer22Inst):
            return "balancer_2_2()"
        if isinstance(i, InfeedOneInst):
            return f"infeed_one({repr_for_nm(i.n, i.m)})"
        if isinstance(i, IgnoreOneInputInst):
            return f"ignore_one_input({repr_for_nm(i.n, i.m)})"
        elif isinstance(i, MultiplexInst):
            return f"multiplex({repr_for_nm(i.in_n, i.in_m)}, {repr_for_nm(i.out_n, i.out_m)}, {i.num_in_copies}, {i.num_out_copies})"


    return graph_for_nm, mermaid_for_nm, repr_for_nm


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Implementing those rules plus a little extra code, we can now look at *low-level* graphs of 2-2 balancers or *high-level* graphs showing how larger balancers are composed of smaller ones:

    Note that the 2-2 balancers are labeled as 0,1,2, ..., etc.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    N = mo.ui.number(start=1, step=1, value=3, label="N (inputs)")
    M = mo.ui.number(start=1, step=1, value=7, label="M (outputs)")
    mo.vstack((N, M))
    return M, N


@app.cell
def _(M, N, balancer_min_nodes, graph_for_nm, mo, repr_for_nm):
    print(f"Minimum number of nodes for a {N.value} to {M.value} balancer: {balancer_min_nodes[N.value, M.value]}")
    print("The graph can be reconstructed in code via:")
    print(repr_for_nm(N.value, M.value))
    # print(graph_for_nm(N.value, M.value).mermaid_str())
    mo.mermaid(graph_for_nm(N.value, M.value).mermaid_str())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here's a high level representation of the N-M balancer:
    """)
    return


@app.cell
def _(M, N, mermaid_for_nm, mo):
    mo.mermaid(mermaid_for_nm(N.value, M.value))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of course it's also a good idea to double check and make sure make sure that these larger balancers actually balance. I also think it's interesting to see how long it takes for balances to reach an equilibrium. For example, when you have a 1-3 balancer (that is a 2-2 balancer with one of its outputs fed to one of its inputs), there's a certain number of edges/hops/steps that some input must go through before it gets from the first 2-2 balancer to the output. Since some of the output as sent in back as input, there will be some proportion of the original input that does not get to the output until many steps later.

    In the graphs below we turn the graph into its matrix form, then for a subset of the inputs, we see how much of that input goes to each output after T steps. We can also measure the "error" by looking at how much of the input has gone to each output versus how much is expected in an N-M balancer.

    Every balancer with multiple layers will take at least as many steps as there are layers for input to go to the output.
    """)
    return


@app.cell(hide_code=True)
def _(M, N, alt, graph_for_nm, graph_to_matrix, mo, np, pd):
    def simulate(n, m, num_steps):
        g = graph_for_nm(n, m)
        mat = graph_to_matrix(g)
        data = []
        expected_steady_state = 1 / n / m
        for input_index in range(n):
            v = np.zeros(len(mat))
            v[input_index] = 1 / n
            for steps in range(num_steps):
                v @= mat
                for output_index in range(m):
                    value = v[len(mat) - m + output_index]
                    data.append(dict(
                        steps=steps,
                        in_out=f"{input_index}:{output_index}",
                        expected=expected_steady_state,
                        error=abs(value - expected_steady_state),
                        value=value
                    ))
        df = pd.DataFrame.from_records(data)
        return df


    simulation = simulate(N.value, M.value, num_steps=50)
    mo.vstack((
        mo.ui.altair_chart(alt.Chart(simulation).mark_line().encode(
            x='steps',
            y='value',
            color='in_out:N'
        )).properties(width=600),
        mo.ui.altair_chart(alt.Chart(simulation).mark_line().encode(
            x='steps',
            y=alt.Y("error").scale(type="log"),
            color='in_out:N'
        )).properties(width=600),
    ))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Conclusion

    And now after all that, we can look a heatmap showing the minimum number of 2-2 balancers that it (probably) takes to create an N-M balancer.
    """)
    return


@app.cell
def _(alt, balancer_min_nodes, np, pd):
    def _chart():
        max_n = max(n for n, _ in balancer_min_nodes)
        max_m = max(m for _, m in balancer_min_nodes)
        ns, ms = np.meshgrid(range(1, min(25, max_n)), range(1, min(45, max_m)))
        num_nodes = [balancer_min_nodes.get((n, m), -10) for n, m in zip(ns.ravel(), ms.ravel())]
        tooltip = [f"{n}-{m}: {r}" for n, m, r in zip(ns.ravel(), ms.ravel(), num_nodes)]

        df = pd.DataFrame({'n': ns.ravel(), 'm': ms.ravel(), 'num_nodes': num_nodes, 'tooltip': tooltip})

        return alt.Chart(df, title="Minimum nodes for balancer with n inputs, m outputs").mark_rect().encode(
            x='m:O',
            y='n:O',
            color='num_nodes:Q',
            tooltip='tooltip',
        )

    _chart()
    return


@app.cell(hide_code=True)
def _(MAX_NODES, mo):
    mo.md(f"""
    And if we want to look at the heatmap much more zoomed out, you get beautiful heatmap below, showing (probably) all the N-M balancers that can be made with {MAX_NODES.value} or fewer 2-2 balances.

    The color scheme is a little custom hack because I like how it looks. In general, the minimum number of nodes you need to make an N-M balancer (N is y-axis and M is x-axis) goes up the further right and down you go (as N or M increase).
    """)
    return


@app.cell(hide_code=True)
def _(balancer_min_nodes, mo, np):
    def _():
        max_n = max(n for n, _ in balancer_min_nodes)
        max_m = max(m for _, m in balancer_min_nodes)
        heatmap = np.zeros((max_n, max_m, 3))
        for (n, m), r in balancer_min_nodes.items():
            heatmap[n - 1, m - 1, :] = r #/ (n + m)**.5
        h, w, _ = heatmap.shape

        # hmax = heatmap.max()
        # heatmap[:, :, 1] = heatmap[:, :, 1] % 2 * hmax / 1
        # heatmap[:, :, 2] = heatmap[:, :, 2] % 4 * hmax / 3

        heatmap /= heatmap.max()
        hmax = 1
        heatmap[:, :, 1] *= 4
        heatmap[:, :, 2] *= 2
        heatmap %= hmax
        return mo.image(heatmap, vmin=0, vmax=heatmap.max(), width=1000)

    _()
    return


if __name__ == "__main__":
    app.run()
