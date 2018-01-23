## Cryptowatch
---

Currently only supports BTC and ETH.

### Design
 - Input addresses into a configuration file (or database)
 - App checks public api for wallet on blockchain
 - Posts TXs to redis (should probably use dynamodb or something more persistent)
 - Any new TXs seen will be sent to an SNS Topic
 - Users subscribe to SNS topic to get notifications


### TODO
 - Metadata for different addresses (the "Why" of tracking a wallet)
