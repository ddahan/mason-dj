# Token Authentication

This is the documentation about how our custom Token authentication work.

### What's for?

This system is made to be used with an API. It allows delivery tokens for accessing the API, 


- [] [Security] For client-side storage, use secure storage mechanisms like HTTPS-only cookies or secure storage in mobile devices.
- [] [Security] Event-based Token Regeneration
- [] [Security] Add Ugent-Agent and IP Checks. Bind tokens to a user's IP address and user agent, adding an extra layer of security. However, this can create usability issues if the user's IP changes frequently.


### Concepts

#### Access Token vs. Refresh Token

The refresh token system doesn't eliminate the risk of token compromise but reduces it by limiting the lifespan and exposure of access tokens and providing a mechanism for securely issuing new ones. It's a strategy that balances security with user experience by reducing the frequency of user logins and the risks associated with long-lived tokens.

- Access Token: A short-lived token that grants access to resources. It typically expires after a short duration (default: 1 hour) to minimize the risk if it gets compromised.
- Refresh Token: A longer-lived token used to obtain new access tokens. This token stays valid for a longer period (default: 1 week) and is used only to get new access tokens.

By having two tokens with different lifespans, a layered security model is created. The access token is like a short-term pass, quickly invalidated, while the refresh token is more like a key that is less frequently used and can be better protected and monitored.

If an access token is compromised, its impact is limited to its short lifespan. The refresh token, although more powerful, is less likely to be exposed and can have additional security checks applied when used.

### Workflow

1. **Initial Authentication**: When a user logs in, the server issues both an access token and a refresh token.
2. **Accessing Resources**: The access token is used for regular interactions with the API. It’s sent with each request to authenticate the user.
3. **Token Expiration**: Once the access token expires, the client can no longer access the API with it.
4. **Token Refresh**: Instead of asking the user to log in again, the client uses the refresh token to request a new access token from the authentication server.
5. **Issuing New Access Token**: The server validates the refresh token and, if it’s valid, issues a new access token (and optionally a new refresh token).

About **revocation** and **regeneration**:
- There is a page to revoque tokens manually
- Event-based revocation (log out, reset password, etc.)
- On each refresh request, the refresh token is regenerated (new created and old one invalidated)


### Notes
- [] settings should be used to change
- [] this app should be externalized
