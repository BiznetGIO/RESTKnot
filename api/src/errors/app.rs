#[derive(Debug)]
pub enum Error {
    // Other
    Internal,

    // Rtype
    RtypeNotFound,
    RtypeAlreadyExists,

    // Ttl
    TtlNotFound,
    TtlAlreadyExists,

    // User
    UserNotFound,
    UsernameAlreadyExists,

    // Record
    RecordNotFound,
    RecordAlreadyExists,

    // Rdata
    RdataNotFound,
    RdataAlreadyExists,

    // Zone
    ZoneNotFound,
    ZoneAlreadyExists,
}

impl std::convert::From<Error> for crate::Error {
    fn from(err: Error) -> Self {
        match err {
            // Ttl
            Error::TtlNotFound => crate::Error::NotFound(String::from("Ttl not found")),
            Error::TtlAlreadyExists => {
                crate::Error::AlreadyExists(String::from("Ttl time is already in use"))
            }

            // Rtype
            Error::RtypeNotFound => crate::Error::NotFound(String::from("Record type not found")),
            Error::RtypeAlreadyExists => {
                crate::Error::AlreadyExists(String::from("Record type time is already in use"))
            }

            // User
            Error::UserNotFound => crate::Error::NotFound(String::from("user not found")),
            Error::UsernameAlreadyExists => {
                crate::Error::AlreadyExists(String::from("username is already in use"))
            }

            // Record
            Error::RecordNotFound => crate::Error::NotFound(String::from("record not found")),
            Error::RecordAlreadyExists => {
                crate::Error::AlreadyExists(String::from("Recordname is already exists"))
            }

            // Rdata
            Error::RdataNotFound => crate::Error::NotFound(String::from("rdata not found")),
            Error::RdataAlreadyExists => {
                crate::Error::AlreadyExists(String::from("Recordname is already exists"))
            }

            // Zone
            Error::ZoneNotFound => crate::Error::NotFound(String::from("Zone not found")),
            Error::ZoneAlreadyExists => {
                crate::Error::AlreadyExists(String::from("Zone is already exists"))
            }

            // Other
            Error::Internal => crate::Error::Internal(String::new()),
        }
    }
}

impl std::convert::From<sqlx::Error> for Error {
    fn from(_err: sqlx::Error) -> Self {
        // Not found error should be catched manually
        Error::Internal
    }
}
