set reg '"subreddit":"(?:ADHD|adhdwomen|aspergirls|AutismTranslated|autismmemes|AutisticPride|Autism|AutisticAdults|autisminwomen|neurodivergent|NeurodivergentLGBTQ)"'

echo "["(date +%F_%r)"] Starting"

rg $reg       \
  --threads=0 \
  --no-filename \
  --no-unicode \
  --no-pcre2 \
  --no-heading \
  --ignore-case \
  --pre-glob '*.zst' \
  --pre "./decompress.sh" &> nd_subreddits.json 

echo "["(date +%F_%r)"] Done!"

