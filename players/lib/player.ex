defmodule Player do

	def new(team, number, x, y) do
		player = [team, number, x, y]
		IO.puts("Spawning player #{number}")
		handle_messages(player)
	end

	def update_position([team, number, x, y]) do
        new_x = Enum.random([-1, 0, 1]) + x
        new_y = Enum.random([-1, 0, 1]) + y
        [team, number, new_x, new_y]
    end

	def handle_messages(player) do
		IO.puts "#{Enum.join(player, ", ")}"
		receive do
	  		{:position, from} ->
	    		send(from, player)
	    		handle_messages(player)
	    	{:move, _from} ->
	    	    new_player = update_position(player)
	    	    handle_messages(new_player)
	    	{:test, _from} ->
	    		IO.puts("TEST, #{player}!")
	    		handle_messages(player)
	    	{msg} ->
	    		IO.puts("GOT, #{msg}!")
	    		handle_messages(player)
		end
	end  

end