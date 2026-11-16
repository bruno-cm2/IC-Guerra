export const TOKEN = "access_token"
export const REFRESH = "refresh_token"

export const isAutenticated = () => localStorage.getItem(TOKEN) !== null
export const getToken = () => localStorage.getItem(TOKEN)