const Endpoints = {
  AUTH: {
    LOGIN: "/auth/login",
    REGISTER: "/auth/register",
    LOGOUT: "/auth/logout",
    REFRESH_TOKEN: "/auth/refresh-token",
    REDEEM_CODE: "/auth/redeem-code",
    REQUEST_CODE:"/auth/request-code",
  },
  USERS: {
    MY_PROFILE: "/users/profile/me",
    MY_FAVORITE: "/users/favorite/me",
  },
  FILMS: {
    GET_FILMS: "/films",
    GET_POSTER: (filmId: number) => `/films/${filmId}/poster`,
    GET_FILM_DETAIL: (filmId: number) => `/films/${filmId}`,
    GET_FILM_TRAILER: (filmId: number) => `/films/${filmId}/trailer`,
    GET_FILM_FILTER_OPTIONS: "/films/filters",
    SEARCH_FILM_SMART: "/films/gigasearch",
  },
}

export default Endpoints
