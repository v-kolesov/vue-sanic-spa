
export function getWebsocketUrl() {
    const protocol = location.protocol == 'http:' ? 'ws' : 'wss'
    return `${protocol}://${location.host}/ws?token=` + localStorage.getItem('token')   
}