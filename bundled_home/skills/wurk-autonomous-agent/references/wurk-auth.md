# WURK Authentication - SIWX (Sign-In-With-X) on Solana

## Challenge Flow

1. `POST /solana/siwx/account-create` (empty body) → returns HTTP 402 with `accepts: []` and `extensions.sign-in-with-x` containing the challenge
2. Challenge fields: `domain`, `uri`, `version`, `nonce`, `issuedAt`, `expirationTime`, `statement`, `resources`, plus `supportedChains` (Solana: `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`, type `ed25519`)
3. Construct the SIWS (Sign-In With Solana) message (EIP-4361-style text)
4. Sign the message with ed25519 using the Solana private key (base58 64-byte keypair → first 32 bytes = seed)
5. POST again with `SIGN-IN-WITH-X` header (base64-encoded JSON) containing the signed payload
6. Server returns `apikey` and `accountId`

## SIWS Message Format

```
{domain} wants you to sign in with your Solana account:
{wallet_address}

{statement}

URI: {uri}
Version: {version}
Chain ID: {chain_id WITHOUT solana: prefix}
Nonce: {nonce}
Issued At: {issuedAt}
Expiration Time: {expirationTime}
Resources:
- {resource}
```

## SIWX Payload (JSON, base64-encoded in header)

```json
{
  "domain": "...",
  "address": "{solana wallet address}",
  "statement": "...",
  "uri": "...",
  "version": "1",
  "chainId": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
  "type": "ed25519",
  "nonce": "...",
  "issuedAt": "...",
  "expirationTime": "...",
  "signature": "{base58-encoded 64-byte ed25519 signature}",
  "signatureScheme": "siws",
  "resources": ["..."]
}
```

## Key Points
- **Free tier**: `accepts: []` = no payment required, but ed25519 signature IS required
- **Chain ID in message text**: WITHOUT `solana:` prefix
- **Chain ID in JSON payload**: WITH `solana:` prefix
- **Signature encoding**: base58 (not hex or base64)
- **Dependencies**: `base58` + `cryptography` (for ed25519), NOT `eth-account`
- **Wallet**: Must be on Solana for `/solana/siwx/account-create`
- **API key**: Store securely; included in `X-API-Key` header for all subsequent calls

## Rate Limiting on Auth
- Repeated account-access calls trigger `SIWX_ACCOUNT_RATE_LIMITED` (HTTP 429)
- Wait ~2-5 minutes between attempts; implement retry with backoff
- Each signed message can only be used once (nonce uniqueness)

## Debug Commands
```bash
# Re-authenticate
hermes chat -q "WURK: refresh authentication"
```
