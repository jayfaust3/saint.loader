package common.models

import java.time.LocalDateTime

case class Saint(
    var _id: String,
    var createdDate: LocalDateTime,
    var modifiedDate: LocalDateTime,
    var active: Boolean,
    var name: String,
    var yearOfBirth: Int,
    var yearOfDeath: Int,
    var region: String,
    var martyred: Boolean,
    var notes: Option[String],
    var hasAvatar: Boolean
)
