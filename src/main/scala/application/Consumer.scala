package application

import java.time.LocalDateTime
import java.util.{Collections, Properties}
import java.util.regex.Pattern
import java.sql._
import org.apache.kafka.clients.consumer.KafkaConsumer
import org.json4s._
import org.json4s.native.Serialization
import org.json4s.native.Serialization.read
import scala.collection.JavaConverters._
import common.models.Saint

object Consumer extends App {
  case object DateSerializer extends CustomSerializer[LocalDateTime](format => (
    {
      case JString(s) => LocalDateTime.parse(s.substring(0, s.length() - 1))
      case JNull => null
    },
    {
      case d: LocalDateTime => JString(d.toString())
    }
    )
  )

  implicit val formats = DefaultFormats + DateSerializer

  val props:Properties = new Properties()

  props.put("group.id", System.getenv("KAFKA_BROKER_GROUP_ID"))
  props.put("bootstrap.servers",s"${System.getenv("KAFKA_BROKER_SERVER_URL")}:${System.getenv("KAFKA_BROKER_PORT")}")
  props.put("key.deserializer","org.apache.kafka.common.serialization.StringDeserializer")
  props.put("value.deserializer","org.apache.kafka.common.serialization.StringDeserializer")
  props.put("enable.auto.commit", "true")
  props.put("auto.commit.interval.ms", "1000")

  val consumer = new KafkaConsumer(props)

  val creationTopic: String = System.getenv("SAINT_CREATION_KAFKA_TOPIC")
  val updateTopic: String = System.getenv("SAINT_UPDATE_KAFKA_TOPIC")
  val deletionTopic: String = System.getenv("SAINT_DELETION_KAFKA_TOPIC")

  val topics = List(creationTopic, updateTopic, deletionTopic)

  try {
    consumer.subscribe(topics.asJava)
    
    while (true) {
      val records = consumer.poll(10)

      for (record <- records.asScala) {
        val recordJSON: String = record.value()

        val deserializedRecord = read[Saint](recordJSON)

        val connection: Connection = DriverManager.getConnection(System.getenv("SAINT_LAKE_DB_CONNECTION_STRING"), System.getenv("SAINT_LAKE_DB_USER"), System.getenv("SAINT_LAKE_DB_PASSWORD"))

        val statement = connection.createStatement()

        statement.execute(s"INSERT INTO ${System.getenv("SAINT_LAKE_DB_TABLE_NAME")} (id, created_date, modified_date, active, name, year_of_birth, year_of_death, region, martyred, notes, has_avatar) VALUES ('${deserializedRecord._id}', '${deserializedRecord.createdDate}', '${deserializedRecord.modifiedDate}', ${deserializedRecord.active}, '${deserializedRecord.name}', ${deserializedRecord.yearOfBirth}, ${deserializedRecord.yearOfDeath}, '${deserializedRecord.region}', ${deserializedRecord.martyred}, '${deserializedRecord.notes.getOrElse("null")}', ${deserializedRecord.hasAvatar});")

        connection.close()
      }
    }
  }catch{
    case e:Exception => e.printStackTrace()
  }finally {
    consumer.close()
  }
}
