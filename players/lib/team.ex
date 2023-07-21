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
        player_info = [team_name, 1, 0, hight / 2]
        pid = spawn(Player, :new, player_info)
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts player_name
        player_info
      n when n in 2..5 ->
        player_info = [team_name, n, width / 8, (n-1) * hight / 8]
        pid = spawn(Player, :new, player_info)
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts player_name
        player_info
      n when n in 6..9 ->
        player_info = [team_name, n, 3 * width / 8, (n-5) * hight / 8]
        pid = spawn(Player, :new, [team_name, n, 3 * width / 8, (n-5) * hight / 8])
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts player_name
        player_info
      n ->
        player_info = [team_name, n, 3 * width / 2, (n-10) * hight / 4]
        pid = spawn(Player, :new, [team_name, n, 3 * width / 2, (n-10) * hight / 4])
        Process.register(pid, player_name)
        IO.inspect pid
        IO.puts "== #{player_name} =="
        player_info
    end
  end

  def ping_players(team_name, msg) do
    IO.puts("PING...")
    for num <- 1..11 do
      IO.inspect(team_name, label: "Team name: ")
      IO.inspect(to_string(num), label: "Number is: ")
      atom_name = String.to_atom(team_name <> to_string(num))
      IO.inspect(atom_name, label: "Atom name is: ")

      case Process.whereis(atom_name) do
        pid when is_pid(pid) ->
            IO.inspect(pid, label: "PID is: ")
            send(pid, {msg, self()})
        nil ->
            IO.puts("Process not found for atom: #{atom_name}")
      end
    end
  end

  def loop(players_info, team_name) do
    receive do
      {:positions, from} ->
        IO.puts "Received message to ping!"
        ping_players(team_name, :position)
        if length(players_info) == 11 do
          send(from, {:blue_team, players_info})
          loop([], team_name)
        else
          loop(players_info, team_name)
        end
      {:move, _from} ->
         ping_players(team_name, :move)
         loop(players_info, team_name)
      {:position, player_msg} ->
        new_players_info = players_info ++ [player_msg]
        loop(new_players_info, team_name)
      {:testing} ->
        ping_players(team_name, :testing)
        loop(players_info, team_name)
      {:end, _} ->
        :ok
    end
  end
end

