defmodule Player do
	#@export new/4

	#defstruct team: "", number: 0, x_pos: 0, y_pos: 0

	def new(team, number, x, y) do
		#player = %Player{team: team, number: number, x_pos: x, y_pos: y}
		player = [team, number, x, y]
		IO.puts("Spawning player #{number}")
		#pid = spawn(__MODULE__, :handle_messages, [player])
		handle_messages(player)
    	#player
	end

	#def get_team(player) do
	#	player.team
	#end

	#def get_number(player) do
	#	player.number
	#end

	#def get_x_pos(player) do
	#	player.x_pos
	#end

	#def get_y_pos(player) do
	#	player.y_pos
	#end

	#def update_position(player, x, y) do
	#	%Player{player | x_pos: x, y_pos: y}
	#end

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