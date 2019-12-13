# This file is very the same as the python script
# It only differs in syntax.

using Random
Random.seed!(2019); # make sure this tutorial is reproducible

using LightGraphs
using StatsBase

N = 100000
avg_d = 14

MCS_STEPS = 10000

c = parse(Float64, ARGS[1])
println("Con c(0)=$c")

q = parse(Int, ARGS[2])
println("Neighbours to consider q=$q")


function agent_move(
    node::Int64,
    p::Float64,
    q::Int64,
    states::Array,
    neighbours::Array
    )
    if Random.rand() < p
        # If p then with prob 1/2 = 1 and with 1/2 = -1
        if Random.rand() < 0.5
            states[node] = states[node] *(-1)
        end
    else
        # Check if we can select q neighbors
        if length(neighbours) < q
            return
        end
        # Get randomly q neighbours
        voters = sample(neighbours, q, replace=false)
        # Check if we should change the state
        S = 0
        for v in voters
            S += states[v]
        end
        if S == q
            states[node] = 1
        elseif S == -q
            states[node] = -1
        end
    end
end

function mcs(graph, N, p, q, states)
    for i in 1:N
        # picka a node
        node = rand(1:N)
        agent_move(
            node,
            p,
            q,
            states,
            neighbors(graph, node)
        )
    end
end

function simulate(graph, N, p, q, n_mcs, states)
    println("Starting simulation")
    for i in 1:n_mcs
        if i%100 == 0
            println("MCS = $i")
        end
        mcs(graph, N, p, q, states)
    end
end

function gen_states(N::Int, c::Float64)::Array
    # function that generates initial states
    states = fill(-1, N)
    for i in sample(1:N, Int(c*N), replace=false)
        states[i] = 1
    end
    states
end

function calc_con(states::Array, N::Int)
    return (1/(2*N))*sum(states) + 0.5
end

function save_results(data, q, c)
    println("Saving results")
    open("results_$(q)_$(c).txt", "w") do f
        write(f, string(data))
    end
end

println("Generating graph")
G = erdos_renyi(N, avg_d/(N-1))

function main(graph)
    results = zeros(60)
    i = 0
    # for p in range(0,stop=0.4, length=60)   # for q = 2
    for p in range(0,stop=0.11, length=60)    # for q = 8
        i += 1
        println("Strarting simulation for i=$i, c=$c, q=$q")
        states = gen_states(N, c)
        simulate(
            graph,
            N,
            p,
            q,
            MCS_STEPS,
            states
        )
        results[i] = calc_con(states, N)
        println("Result $(results[i])")
    end
    save_results(results, q, c)
end

main(G)

# @async main(G, 1.0, 2)
# @async main(G, 0.5, 2)
# @async main(G, 1.0, 8)
# @async main(G, 0.5, 8)
