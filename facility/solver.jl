using JuMP
using Gurobi
using Base.Test
using StatsBase

function solverGreedy(fname)
    fin = "/Users/shunyong/ACE/Coursera/Discrete Optimization/facility/" * fname
    f = open(fin, "r")
    raw = split(readline(f), ' ')
    N = int(raw[1])
    M = int(raw[2])

    println("Number of Facility: ", N)
    println("Number of Custormer: ", M)

    data = readdlm(fin, ' ', skipstart = 1)
    sData = data[1:N, 1:4]
    cData = data[(N + 1):(N + M), 1:3]

    dist = zeros(N, M)
    for i = 1 : N
        for j = 1 : M
            dist[i, j] = norm(sData[i, 3:4] - cData[j, 2:3])
        end
    end

    # Create Gurobi model

    m = Model(solver = GurobiSolver(OutputFlag=0))

    @defVar(m, 0 <= x[1:N, 1:M] <= 1, Int)
    @defVar(m, 0 <= y[1:N] <= 1)

    # objective
    @setObjective(m, Min, sum{dist[i,j]*x[i,j], i=1:N, j=1:M} + sum{sData[i,1] * y[i], i = 1:N})

    # constraint
    for i = 1 : N
        @addConstraint(m, sum{cData[j, 1]*x[i, j], j = 1:M} <= sData[i, 2] * y[i])
    end

    for j = 1 : M
        @addConstraint(m, sum{x[i, j], i=1:N} == 1)
    end

    function corners(cb)
        sol = getValue(y)
        tmp = 0.0
        idx = 1
        for i = 1:N
            if sol[i] < 1 && tmp < sol[i] * sData[i, 2] / sData[i, 1]
                tmp = sol[i] * sData[i, 2] / sData[i, 1]
                idx = i
            end
        end
        if tmp > 0.0
            # Add the new subtour elimination constraint we built
            @addLazyConstraint(cb, y[idx] == 1)
        end
    end

    # Solve the problem with our cut generator
    addLazyCallback(m, corners)

    solve(m)

    cost = int(getObjectiveValue(m))
    x_mat = getValue(x)
    sol = int(zeros(M))
    for i = 1:N
        for j = 1:M
            if x_mat[i, j] == 1
                sol[j] = int(i)
            end
        end
    end

    println("$cost 0")
    println(join((sol - 1), " "))

    # write data into file
    outfile = open("/Users/shunyong/ACE/Coursera/Discrete Optimization/facility/" * fname * "_sol", "w")
    write(outfile, "$cost 0", "\n")
    write(outfile, join((sol - 1), " "))
    close(outfile)
end

function solver(fname)
    fin = "/Users/shunyong/ACE/Coursera/Discrete Optimization/facility/" * fname
    f = open(fin, "r")
    raw = split(readline(f), ' ')
    N = int(raw[1])
    M = int(raw[2])

    println(M, N)

    data = readdlm(fin, ' ', skipstart = 1)
    sData = data[1:N, 1:4]
    cData = data[(N + 1):(N + M), 1:3]

    # tour, dist = solveflp(N, M, sData, cData)

    ################

    dist = zeros(N, M)
    for i = 1 : N
        for j = 1 : M
            dist[i, j] = norm(sData[i, 3:4] - cData[j, 2:3])
        end
    end

    # Create Gurobi model

    m = Model(solver = GurobiSolver(IterationLimit=50000))

    @defVar(m, x[1:N, 1:M], Bin)
    @defVar(m, y[1:N], Bin)

    # objective
    @setObjective(m, Min, sum{dist[i,j]*x[i,j], i=1:N, j=1:M} + sum{sData[i,1] * y[i], i = 1:N})

    # constraint
    for i = 1 : N
        @addConstraint(m, sum{cData[j, 1]*x[i, j], j = 1:M} <= sData[i, 2] * y[i])
    end

    for j = 1 : M
        @addConstraint(m, sum{x[i, j], i=1:N} == 1)
    end

    status = solve(m)
    println(getValue(x))
    println(getValue(y))
    cost = int(getObjectiveValue(m))
    sol = int(zeros(M))
	  for i = 1:N
        for j = 1:M
            if getValue(x)[i, j] == 1
                sol[j] = int(i)
            end
        end
    end

    println("$cost 0")
    println(join((sol - 1), " "))

    # write data into file
    outfile = open("/Users/shunyong/ACE/Coursera/Discrete Optimization/facility/" * fname * "_sol", "w")
    write(outfile, "$cost 0", "\n")
    write(outfile, join((sol - 1), " "))
    close(outfile)
end

solverGreedy(ARGS[1])
