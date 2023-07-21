defmodule Game do
  def start_link(width, height) do
    spawn_link(__MODULE__, :init, [width, height])
  end

  def init(width, height) do
    Process.register(spawn(Team, :init, ["Blue", width, height]), :blue_team_pid)
    #Process.register(:red_team_pid, spawn(Team, :new, ["Red", width, height]))
    loop(%{:red_team => [], :blue_team => []})
  end

  def print_number_and_coordinates_list(list_of_elements) do
    formatted_data = Enum.map(list_of_elements, fn [_, number, x, y] ->
        "Number: #{number}\nX: #{x}, Y: #{y}\n"
    end)
    IO.puts(Enum.join(formatted_data, "\n"))
  end
  
  defp loop(map_of_positions) do
    receive do
      {:positions, from} ->
        IO.puts "Received message!"
        send(:blue_team_pid, {:positions, self()})
        #send(:red_team_pid, {:positions, self()})
        send(from, {:position_reply, map_of_positions})
        loop(Map.new(map_of_positions, fn {key, _value} -> {key, []} end))
      {:move} ->
        send(:blue_team_pid, {:move, self()})
        loop(map_of_positions)

      {:blue_team, players_list} ->
        IO.puts "Received message from BLUE!"
        print_number_and_coordinates_list(players_list)
        map_of_positions = Map.put(map_of_positions, :blue_team, players_list)
        loop(map_of_positions)
      {:red_team, players_list} ->
        IO.puts "Received message from RED!"
        map_of_positions = Map.put(map_of_positions, :red_team, players_list)
        loop(map_of_positions)
      {:end, _} ->
        IO.puts "Received message to TERMINATE!"
        :ok
    end
  end
end