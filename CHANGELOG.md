# Changelog

<!--next-version-placeholder-->

## v0.6.0 (2021-09-20)
### Feature
* **test_hash_rate:** Add function to test hash rate of "salt_finder" ([`068b30d`](https://github.com/jojoee/raritygems/commit/068b30d6643801f892ddfadaa90d39ef8911a4e0))
* **mine:** Add parameter n to control number of iterations that will be restarted ([`5e2d1d7`](https://github.com/jojoee/raritygems/commit/5e2d1d7b35720f09fb6b640a25483557ddaab89f))

### Documentation
* **readme:** Update and replace "Usage on Google Colab" with "Run on Google Colab" section ([`83bd5b6`](https://github.com/jojoee/raritygems/commit/83bd5b671d7dbb3f68a37a8d92e72bda60f2673f))
* **readme:** Update "raritygems_salt_finder" section ([`adef60b`](https://github.com/jojoee/raritygems/commit/adef60ba902a72f3dec96cdaa2e8243590e4e933))
* **readme:** Add "Other projects" section into readme.md ([`56c7ae0`](https://github.com/jojoee/raritygems/commit/56c7ae084cc5bf0e4bf986075ff27f4a8e722c81))

## v0.5.0 (2021-09-17)
### Feature
* **performance:** And "iterations per second" text when run it in debug mode ([`19465f1`](https://github.com/jojoee/raritygems/commit/19465f14a982309d5dc5fc884057809efc9c8831))
* **restart:** The process will restart every ~2 hrs to update the gem value ([`66d9b92`](https://github.com/jojoee/raritygems/commit/66d9b92155768550063c4233bddc8b7a9c1c3bc2))
* **message:** Update notification message a bit ([`723a202`](https://github.com/jojoee/raritygems/commit/723a2027eb2d8dbfe96023e71c9ac7ad11ab5f36))

### Documentation
* **readme:** Update public "salt_finder" url and example of "salt_finder" cmd ([`fd45327`](https://github.com/jojoee/raritygems/commit/fd453276deda5b4e284a9fdbd95287488f9783c0))

## v0.4.0 (2021-09-16)
### Feature
* **privatekey:** Force exit when found a salt if not provide a private key ([`747e7f3`](https://github.com/jojoee/raritygems/commit/747e7f382d92d46399a6deb5057ff3c4532b1627))

### Documentation
* **install:** Install with latest version instead of specific version ([`e399446`](https://github.com/jojoee/raritygems/commit/e399446525eb383b53807e6f446c2f0a20c91505))
* **readme:** Init readme doc ([`a3c5b24`](https://github.com/jojoee/raritygems/commit/a3c5b245e3aab6dd46f2386a7f751a63754c7126))

## v0.3.0 (2021-09-16)
### Feature
* **autosign:** Display tx when claim a gem ([`1d5b249`](https://github.com/jojoee/raritygems/commit/1d5b24901bfab3c7142ed483abe90fe3ccd2ea4e))

## v0.2.1 (2021-09-16)
### Fix
* **helper:** ModuleNotFoundError: No module named 'helper' ([`c5c4c9f`](https://github.com/jojoee/raritygems/commit/c5c4c9f89608bd8dd26d2da127518a3944d93638))

## v0.2.0 (2021-09-16)
### Feature
* **raritygems:** Integrate with salt_finder ([`1cf9deb`](https://github.com/jojoee/raritygems/commit/1cf9deb5f6ddf507d099365505b82381ef3a220b))
* **notification:** Dont send LINE notification when line_token is not provided ([`7725548`](https://github.com/jojoee/raritygems/commit/7725548e4440fc5dd8a97e0ca68a2e8c7dd09597))
* **saltfinder:** Add version 1 of saltfinder ([`e9bf45f`](https://github.com/jojoee/raritygems/commit/e9bf45fd607052a3c16e1b428868063a2260acd8))

### Fix
* **web3:** Get_transaction_count function not found ([`a41bca6`](https://github.com/jojoee/raritygems/commit/a41bca6999c5cafabbe3016385370425aeea562e))

## v0.1.0 (2021-09-15)
### Feature
* **miner:** Verison 1 of Miner class ([`f9bf794`](https://github.com/jojoee/raritygems/commit/f9bf794c3b2b71c810fe96e046bbd0d26f1a8975))

### Fix
* **helper:** Add missing helper files ([`35a3693`](https://github.com/jojoee/raritygems/commit/35a3693dbb96d74f8cad9b0ea3e59c9712d3a9a1))

### Performance
* Increase iterations per second by using golang instead ([`17b8109`](https://github.com/jojoee/raritygems/commit/17b8109dfb5c0a0f259d9168869db97ac6440bc3))
