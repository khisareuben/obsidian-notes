

```kotlin

import kotlinx.serialization.*
import kotlinx.serialization.json.*
import java.io.File

@Serializable
data class MediaList(val items: MutableList<String> = mutableListOf())

fun loadList(filename: String): MediaList {
    val file = File(filename)
    return if (file.exists()) {
        try {
            Json.decodeFromString(MediaList.serializer(), file.readText())
        } catch (e: Exception) {
            println("Error reading $filename. Starting with an empty list.")
            MediaList()
        }
    } else {
        MediaList()
    }
}

fun saveList(filename: String, list: MediaList) {
    val file = File(filename)
    file.writeText(Json.encodeToString(MediaList.serializer(), list))
}

fun main() {
    var anime = loadList("anime_list.json")
    var manhwa = loadList("manhwa_list.json")

    println("-------------------- WELCOME TO MY ANIME AND MANHWA LIST --------------------")

    while (true) {
        println("\n1. Anime\n2. Manhwa\n3. Exit")
        print("Enter your choice: ")
        val choice = readLine()?.toIntOrNull() ?: continue

        when (choice) {
            1 -> {
                while (true) {
                    println("\n1. Search for an anime\n2. Show all animes\n3. Add a new anime\n4. Back to main menu")
                    print("Enter your choice: ")
                    val choice2 = readLine()?.toIntOrNull() ?: continue

                    when (choice2) {
                        1 -> {
                            print("Enter the name of the anime: ")
                            val search = readLine()?.lowercase() ?: ""
                            if (anime.items.contains(search)) {
                                println("$search is in the list.")
                            } else {
                                println("Anime not found.")
                            }
                        }
                        2 -> {
                            println("Animes available: ${anime.items.size}")
                            anime.items.forEachIndexed { i, item -> println("\t${i + 1}. $item") }
                        }
                        3 -> {
                            print("Enter the name of the new anime: ")
                            val newAnime = readLine()?.lowercase() ?: ""
                            anime.items.add(newAnime)
                            saveList("anime_list.json", anime)
                            println("$newAnime has been added.")
                        }
                        4 -> break
                        else -> println("Invalid choice.")
                    }
                }
            }
            2 -> {
                while (true) {
                    println("\n1. Search for a manhwa\n2. Show all manhwas\n3. Add a new manhwa\n4. Back to main menu")
                    print("Enter your choice: ")
                    val choice3 = readLine()?.toIntOrNull() ?: continue

                    when (choice3) {
                        1 -> {
                            print("Enter the name of the manhwa: ")
                            val search = readLine()?.lowercase() ?: ""
                            if (manhwa.items.contains(search)) {
                                println("$search is in the list.")
                            } else {
                                println("$search is not in the list.")
                            }
                        }
                        2 -> {
                            println("Manhwas available: ${manhwa.items.size}")
                            manhwa.items.forEachIndexed { i, item -> println("\t${i + 1}. $item") }
                        }
                        3 -> {
                            print("Enter the name of the new manhwa: ")
                            val newManhwa = readLine()?.lowercase() ?: ""
                            manhwa.items.add(newManhwa)
                            saveList("manhwa_list.json", manhwa)
                            println("$newManhwa has been added.")
                        }
                        4 -> break
                        else -> println("Invalid choice.")
                    }
                }
            }
            3 -> {
                print("Do you want to exit the program? (yes/no): ")
                val exit = readLine()?.lowercase()
                if (exit == "yes") {
                    println("Exiting the program...")
                    break
                }
            }
            else -> println("Invalid choice.")
        }
    }
}


```