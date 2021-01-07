SQL_USERS_TABLE = """
                    CREATE TABLE IF NOT EXISTS Users (
                        IdUser INTEGER PRIMARY KEY AUTOINCREMENT,
                        Login TEXT NOT NULL,
                        Password TEXT NOT NULL,
                        Email TEXT NOT NULL,
                        Gender TEXT NOT NULL,
                        Height REAL NOT NULL,
                        Age INTEGER NOT NULL,
                        PhysicalActivity INTEGER NOT NULL,
                        Goal INTEGER NOT NULL,
                        Avatar BLOB NOT NULL,
                        UNIQUE(Login)
                    ); 
                  """

SQL_WEIGHTS_TABLE = """
                    CREATE TABLE IF NOT EXISTS Weights (
                        IdWeight INTEGER PRIMARY KEY AUTOINCREMENT,
                        IdUser INTEGER NOT NULL,
                        WeightValue REAL NOT NULL,
                        WeightDate TEXT NOT NULL,
                        FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                    );
                    """

SQL_GDAS_TABLE = """
                    CREATE TABLE IF NOT EXISTS GDAs (
                        IdGDA INTEGER PRIMARY KEY AUTOINCREMENT,
                        IdUser INTEGER NOT NULL,
                        GDAValue INTEGER NOT NULL,
                        GDADate TEXT NOT NULL,
                        FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                    );
                 """

SQL_TRAINING_TYPES_TABLE = """
                            CREATE TABLE IF NOT EXISTS TrainingTypes (
                                IdTrainingType INTEGER PRIMARY KEY AUTOINCREMENT,
                                TrainingName TEXT NOT NULL,
                                BurnedCaloriesPerMinPerKg REAL NOT NULL,
                                UNIQUE(TrainingName)
                            );
                           """

SQL_TRAININGS_TABLE = """
                        CREATE TABLE IF NOT EXISTS Trainings (
                            IdTraining INTEGER PRIMARY KEY AUTOINCREMENT,
                            IdUser INTEGER NOT NULL,
                            IdTrainingType INTEGER NOT NULL,
                            DurationInMin INTEGER NOT NULL,
                            TrainingDate TEXT NOT NULL,
                            FOREIGN KEY (IdUser) REFERENCES Users (IdUser),
                            FOREIGN KEY (IdTrainingType) REFERENCES TrainingTypes (IdTrainingType)
                        );
                      """

SQL_PRODUCTS_TABLE = """
                        CREATE TABLE IF NOT EXISTS Products (
                            IdProduct INTEGER PRIMARY KEY AUTOINCREMENT,
                            IdUser INTEGER NOT NULL,
                            ProductName TEXT NOT NULL,
                            Calories INTEGER NOT NULL,
                            Image BLOB NOT NULL,
                            GlycemicIndexRating INTEGER NOT NULL,
                            FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                        );
                     """

SQL_DISHES_TABLE = """
                    CREATE TABLE IF NOT EXISTS Dishes (
                        IdDish INTEGER PRIMARY KEY AUTOINCREMENT,
                        IdUser INTEGER NOT NULL,
                        DishName TEXT NOT NULL,
                        Image BLOB NOT NULL,
                        GlycemicIndexRating INTEGER NOT NULL,
                        FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                    );
                   """

SQL_DISHES_PRODUCTS_TABLE = """
                            CREATE TABLE IF NOT EXISTS DishesProducts (
                                IdDishesProducts INTEGER PRIMARY KEY AUTOINCREMENT,
                                IdDish INTEGER NOT NULL,
                                IdProduct INTEGER NOT NULL,
                                ProductGrammage INTEGER NOT NULL,
                                FOREIGN KEY (IdDish) REFERENCES Dishes (IdDish),
                                FOREIGN KEY (IdProduct) REFERENCES Products (IdProduct)
                            );
                            """

SQL_CONSUMED_PRODUCTS_TABLE = """
                                CREATE TABLE IF NOT EXISTS ConsumedProducts (
                                    IdConsumedProduct INTEGER PRIMARY KEY AUTOINCREMENT,
                                    IdProduct INTEGER NOT NULL,
                                    IdUser INTEGER NOT NULL,
                                    ConsumptionDate TEXT NOT NULL,
                                    ProductGrammage INTEGER NOT NULL,
                                    FOREIGN KEY (IdProduct) REFERENCES Products (IdProduct),
                                    FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                                );
                              """

SQL_CONSUMED_DISHES_TABLE = """
                            CREATE TABLE IF NOT EXISTS ConsumedDishes (
                                IdConsumedDish INTEGER PRIMARY KEY AUTOINCREMENT,
                                IdDish INTEGER NOT NULL,
                                IdUser INTEGER NOT NULL,
                                ConsumptionDate TEXT NOT NULL,
                                DishGrammage INTEGER NOT NULL,
                                FOREIGN KEY (IdDish) REFERENCES Dishes (IdDish),
                                FOREIGN KEY (IdUser) REFERENCES Users (IdUser)
                            );
                            """