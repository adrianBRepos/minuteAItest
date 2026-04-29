import { type UserAuthorisationResult } from '@i-dot-ai-npm/utilities'

export async function parseAuthToken(
  token: string
): Promise<UserAuthorisationResult | null> {
  if (!token) {
    console.error('No auth token provided to parse')
    return null
  }

  try {
    const parts = token.split('.')
    if (parts.length !== 3) {
      console.error('Invalid JWT token format')
      return null
    }

    const payload = JSON.parse(
      Buffer.from(parts[1], 'base64').toString('utf-8')
    )

    const email = payload.email

    if (!email) {
      console.error('No email found in JWT token payload')
      return null
    }

    console.info(`Successfully parsed token for user: ${email}`)

    return {
      email: email,
      isAuthorised: true,
      authReason: 'ALB_OIDC_AUTHENTICATED',
    }
  } catch (error) {
    console.error('Error parsing auth token:', error)
    return null
  }
}
