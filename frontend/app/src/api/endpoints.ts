const Endpoints = {
    AUTH: {
        LOGIN: '/auth/login',
        REGISTER: '/auth/register',
        LOGOUT: '/auth/logout',
        REFRESH_TOKEN: '/auth/refresh-token',
    },
    USERS: {
        MY_PROFILE: '/users/profile/me'
    },
    FILMS: {
        GET_FILMS: '/films',
        GET_POSTER: (filmId: number) => `/films/${filmId}/poster`
    }
}

export default Endpoints