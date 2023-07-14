defmodule Player do

	def new(team, number, x, y) do
		#player = %Player{team: team, number: number, x_pos: x, y_pos: y}
		player = [team, number, x, y]
		IO.puts("Spawning player #{number}")
		#pid = spawn(__MODULE__, :handle_messages, [player])
		handle_messages(player)
	end

	def handle_messages(player) do
		IO.puts "#{Enum.join(player, ", ")}"
		receive do
	  		{:position, from} ->
	  			IO.puts("Hello, world!")
	    		send(from, player)
	    		handle_messages(player)
	    	{:test, _from} ->
	    		IO.puts("TEST, #{player}!")
	    		handle_messages(player)
	    	{msg} ->
	    		IO.puts("GOT, #{msg}!")
	    		handle_messages(player)
		end
	end  

end