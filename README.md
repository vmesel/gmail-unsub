# GMAIL Unsub

Unsubscribe from major e-mail marketers using two scripts.

## How to use

Generate your credentials.json from Google Cloud APIs with GMail permission, then
save your credentials.json in the .secrets folder. Copy your .env.sample to .env and
fill it with your e-mail.

```
# .env content
YOUR_GMAIL=my_awesome@gmail.com
```

Then, to generate your unsubscription list run:

```
make generate
```

To unsubscribe from all of the e-mails from the generated CSV:

```
make unsub
```

## Roadmap

- Implement basic unsubscribe :heavy_check_mark:
- Create script to iterate on the generated CSV (to be done)
- Create function to access HTTP/HTTPS pages and click on the unsubscription process (to be done)