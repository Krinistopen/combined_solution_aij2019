import numpy as np
import time
import warnings

from solvers import *
from utils import *


def zero_if_exception(scorer):
    def new_scorer(*args, **kwargs):
        try:
            return scorer(*args, **kwargs)
        except:
            return 0

    return new_scorer


class Evaluation(object):
    def __init__(
        self,
        train_path="public_set/train",
        test_path="test_data",
        score_filename="scoring.json",
    ):
        self.train_path = train_path
        self.test_path = test_path
        self.score_filename = score_filename
        self.secondary_score = read_config(self.score_filename)["secondary_score"]
        self.test_scores = []
        self.first_scores = []
        self.secondary_scores = []
        self.classifier = classifier.Solver()
        self.solvers = []
        self.solver_classes = [
            solver1,
            solver2,
            solver3,
            solver4,
            solver5,
            solver6,
            solver7,
            solver8,
            solver9,
            solver10,
            solver11,
            solver11,
            solver13,
            solver14,
            solver15,
            solver16,
            solver17,
            solver17,
            solver17,
            solver17,
            solver21,
            solver22,
            solver23,
            solver24,
            solver25,
            solver26,
            solver27
        ]
        self.time_limit_is_ok = True
        self.time_limit_is_observed = self.solver_loading()
        if self.time_limit_is_observed:
            print("Time limit of fitting is OK")
        else:
            self.time_limit_is_ok = False
            print("TIMEOUT: Some solvers fit longer than 10m!")
        self.clf_fitting()

    def solver_loading(self):
        time_limit_is_observed = True
        for i, solver_class in enumerate(self.solver_classes):
            start = time.time()
            solver_index = i + 1
            train_tasks = load_tasks(self.train_path, task_num=solver_index)
            solver = solver_class.Solver()
            if hasattr(solver, "load"):
                print("Loading Solver {}...".format(solver_index))
                solver.load()
            else:
                print("Fitting Solver {}...".format(solver_index))
                solver.fit(train_tasks)
            duration = time.time() - start
            if duration > 60:
                time_limit_is_observed = False
                print(
                    "Time limit is violated in solver {} which has been fitting for {}m {:2}s".format(
                        solver_index, int(duration // 60), duration % 60
                    )
                )
            print("Solver {} is ready!\n".format(solver_index))
            self.solvers.append(solver)
        return time_limit_is_observed

    def clf_fitting(self):
        tasks = []
        for filename in os.listdir(self.train_path):
            if filename.endswith(".json"):
                data = read_config(os.path.join(self.train_path, filename))
                tasks.append(data)
        print("Fitting Classifier...")
        self.classifier.fit(tasks)
        print("Classifier is ready!")

    # для всех заданий с 1 баллом
    @zero_if_exception
    def get_score(self, y_true, prediction):
        if "correct" in y_true:
            if y_true["correct"] == prediction:
                return 1
        elif "correct_variants" in y_true and isinstance(
            y_true["correct_variants"][0], str
        ):
            if prediction in y_true["correct_variants"]:
                return 1
        elif "correct_variants" in y_true and isinstance(
            y_true["correct_variants"][0], list
        ):
            y_true = set(y_true["correct_variants"][0])
            y_pred = set(prediction)
            return int(
                len(set.intersection(y_true, y_pred)) == len(y_true) == len(y_pred)
            )
        return 0

    # для 8 и 26 заданий
    @zero_if_exception
    def get_matching_score(self, y_true, pred):
        score = 0
        y_true = y_true["correct"]
        if len(y_true) != len(pred):
            return 0
        for y in y_true:
            if y_true[y] == pred[y]:
                score += 1
        return score

    # для 16 задания
    @zero_if_exception
    def get_multiple_score(self, y_true, y_pred):
        y_true = (
            y_true["correct_variants"][0]
            if "correct_variants" in y_true
            else y_true["correct"]
        )
        while len(y_pred) < len(y_true):
            y_pred.append(-1)
        return max(
            0,
            len(set.intersection(set(y_true), set(y_pred))) - len(y_pred) + len(y_true),
        )

    def variant_score(self, variant_scores):
        first_score = sum(variant_scores)
        mean_score = round(np.mean(variant_scores), 3)
        secondary_score = int(self.secondary_score[str(first_score)])
        scores = {
            "first_score": first_score,
            "mean_accuracy": mean_score,
            "secondary_score": secondary_score,
        }
        self.first_scores.append(first_score)
        self.secondary_scores.append(secondary_score)
        return scores

    def get_overall_scores(self):
        for variant, variant_scores in enumerate(self.test_scores):
            scores = self.variant_score(variant_scores)
            print("***YOUR RESULTS***")
            print("Variant: {}".format(variant + 1))
            print("Scores: {}\n".format(scores))

    def predict_from_baseline(self):
        time_limit_is_observed = True
        for filename in os.listdir(self.test_path):
            predictions = []
            print("Solving {}".format(filename))
            data = read_config(os.path.join(self.test_path, filename))[:-1]
            task_number = self.classifier.predict(data)
            for i, task in enumerate(data):
                start = time.time()
                task_index, task_type = i + 1, task["question"]["type"]
                print("Predicting task {}...".format(task_index))
                y_true = task["solution"]
                try:
                    prediction = self.solvers[task_number[i] - 1].predict_from_model(task)
                except:
                    print("Solver {} failed to solve task №{}".format(task_number[i], task_index))
                    prediction = ""
                if task_type == "matching":
                    score = self.get_matching_score(y_true, prediction)
                elif task_index == 16:
                    score = self.get_multiple_score(y_true, prediction)
                else:
                    score = self.get_score(y_true, prediction)
                print(
                    "Score: {}\nCorrect: {}\nPrediction: {}\n".format(
                        score, y_true, prediction
                    )
                )
                predictions.append(score)
                duration = time.time() - start
                if duration > 60:
                    time_limit_is_observed = False
                    self.time_limit_is_ok = False
                    print(
                        "Time limit is violated in solver {} which has been predicting for {}m {:2}s".format(
                            i + 1, int(duration // 60), duration % 60
                        )
                    )
            self.test_scores.append(predictions)
        return time_limit_is_observed


def main():
    warnings.filterwarnings("ignore")
    eval = Evaluation()
    time_limit_is_observed = eval.predict_from_baseline()
    if not time_limit_is_observed:
        print("TIMEOUT: some solvers predict longer then 60s!")
    eval.get_overall_scores()
    mean_first_score = np.mean(eval.first_scores)
    mean_secondary_score = np.mean(eval.secondary_scores)
    print("Mean First Score: {}".format(mean_first_score))
    print("Mean Secondary Score: {}".format(mean_secondary_score))

    if eval.time_limit_is_ok:
        print("Time limit is not broken by any of the solvers.")
    else:
        print("TIMEOUT: Time limit by violated in some of the solvers.")


if __name__ == "__main__":
    main()
