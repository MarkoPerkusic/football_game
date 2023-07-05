defmodule Team do
  def start_link(team_name, width, hight) do
    spawn_link(__MODULE__, :init, [team_name, width, hight])
  end

  def init(team_name, width, hight) do
    players_info = for numbr <- 1..11, do: set_up(numbr, team_name, width, hight)
    loop(players_info, team_name)
  end

  def set_up(numbr, team_name, width, hight) do
    IO.puts "SETTING UP"
    player_name = String.to_atom(team_name <> to_string(numbr))
    IO.puts(player_name)
    case numbr do
      1 ->
        pid = spawn(Player, :new, [team_name, 1, 0, hight / 2])
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts player_name
      n when n in 2..5 ->
        pid = spawn(Player, :new, [team_name, n, width / 8, (n-1) * hight / 8])
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts player_name
      n when n in 6..9 ->
        pid = spawn(Player, :new, [team_name, n, 3 * width / 8, (n-5) * hight / 8])
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts player_name
      n ->
        pid = spawn(Player, :new, [team_name, n, 3 * width / 2, (n-10) * hight / 4])
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts "== #{player_name} =="
    end
  end

  def ping_players(team_name) do
  #def ping_players(players_info) do
    IO.puts("PING...")
    for num <- 1..11 do
      #IO.puts("PING: #{num}! #{String.to_atom(team_name <> to_string(num))}")
      IO.inspect Process.whereis(String.to_atom(team_name <> to_string(num)))
      send(Process.whereis(String.to_atom(team_name <> to_string(num))), {:position, self()})
    end
    #for alias_pid <- players_info, do: send(alias_pid, {:position, self()})
  end
  
  def loop(players_info, team_name) do
    receive do
      {:positions, from} ->
        IO.puts "Received message to ping!"
        ping_players(players_info)
        if length(players_info) == 11 do
          send(from, {:blue_team, players_info})
          loop([], team_name)
        else
          loop(players_info, team_name)
        end 
      {:position, player_msg} ->
        new_players_info = players_info ++ [player_msg]
        loop(new_players_info, team_name)
      {:testing} ->
        ping_players(team_name)
        loop(players_info, team_name)
      {:end, _} ->
        :ok
    end
  end
end

#for num <- 1..11 do IO.puts("PING: #{num}! #{String.to_atom("team_name" <> to_string(num))}") send(String.to_atom("self"), {n}) end
