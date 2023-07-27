defmodule MyApp.Repo do
  use Ecto.Repo,
    otp_app: :players,
    adapter: Ecto.Adapters.Postgres
end

