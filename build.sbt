name := "app"

version := "0.0.1"

scalaVersion := "2.13.3"

mainClass in Compile := Some("application.Consumer")

scalacOptions ++= Seq("-encoding", "UTF-8")

libraryDependencies ++= Seq(
    "org.apache.kafka" % "kafka-clients" % "2.1.0",
    "org.postgresql" % "postgresql" % "42.2.10",
    "org.json4s" %% "json4s-native" % "4.1.0-M1")
