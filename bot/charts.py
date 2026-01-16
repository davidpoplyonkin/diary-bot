import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.formatting import Text, Bold, as_list
from datetime import datetime
from PIL import Image

from apps.diary.models import HealthMetric
from apps.core.models import User
from globals import HEALTH_METRICS

async def reply_chart(
        message: Message,
        user_tg_id: int,
        metric: str,
        date: datetime,
        window: int
    ):
    if metric in ["sbpm", "dbpm", "pm", "sbpe", "dbpe", "pe"]:
        time_of_day = metric[-1] # "m" for morning, "e" for evening
        metric = f"sbp{time_of_day}"

        sbp_rows = await HealthMetric.get_recent(
            user_tg_id=user_tg_id,
            metric=f"sbp{time_of_day}",
            date=date,
            window=window
        )
        dbp_rows = await HealthMetric.get_recent(
            user_tg_id=user_tg_id,
            metric=f"dbp{time_of_day}",
            date=date,
            window=window
        )
        p_rows = await HealthMetric.get_recent(
            user_tg_id=user_tg_id,
            metric=f"p{time_of_day}",
            date=date,
            window=window
        )
        rows = sbp_rows + dbp_rows + p_rows

        # Store the data in a dataframe
        df = pd.DataFrame(rows, columns=rows[0].keys())

        # Reshape the dataframe
        df = df.pivot(index="date", columns="metric", values="value")

        sns.set_theme(style="ticks")
        sns.jointplot(
            x=f"sbp{time_of_day}",
            y=f"dbp{time_of_day}",
            data=df,
            kind="hex",
            color="#4CB391",
        )

        plt.xlabel("SBP")
        plt.ylabel("DBP")
        plt.tight_layout()

        buffer_joint = BytesIO()
        plt.savefig(buffer_joint, format="png")
        plt.close()
        img_joint = Image.open(buffer_joint)

        sns.histplot(
            x=f"p{time_of_day}",
            data=df,
        )
        plt.xlabel("Pulse")
        plt.tight_layout()

        buffer_hist = BytesIO()
        plt.savefig(buffer_hist, format="png")
        plt.close()
        img_hist = Image.open(buffer_hist)

        # Resize the histplot
        w_target = img_joint.width
        h_target = int(img_hist.height * (w_target / img_hist.width))
        img_hist_resized = img_hist.resize((w_target, h_target), Image.Resampling.LANCZOS)

        # Create canvas and paste
        combined_img = Image.new('RGB', (w_target, img_joint.height + h_target), (255, 255, 255))
        combined_img.paste(img_joint, (0, 0))
        combined_img.paste(img_hist_resized, (0, img_joint.height))

        buffer = BytesIO()

        combined_img.save(buffer, format="PNG")
        
    elif metric in ["weight", "glf", "glp", "ttr"]:
        # Retrieve data from the database
        rows = await HealthMetric.get_recent(
            user_tg_id=user_tg_id,
            metric=metric,
            date=date,
            window=window
        )

        # Store the data in a dataframe
        df = pd.DataFrame(rows, columns=rows[0].keys())

        # Change the type of the date column
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

        # Create the chart
        sns.lineplot(x="date", y="value", data=df)

        label_dict = {
            "weight": "Weight (kg)",
            "glf": "Glucose (fasting)",
            "glp": "Glucose (postprandial)",
            "ttr": "Testosterone"
        }

        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Date")
        plt.ylabel(label_dict.get(metric))

        plt.tight_layout()

        buffer = BytesIO()
        
        plt.savefig(buffer, format="png")
        plt.close()
    else:
        msg_text = Text(f"The chart for the metric \"{metric}\" is not yet implemented.")
        msg_kwargs = msg_text.as_kwargs()

        # Notify the admin that there is no chart for the chosen metric
        await message.answer(**msg_kwargs)

        return

    chart_file = BufferedInputFile(
        file=buffer.getvalue(),
        filename="chart"
    )

    user = await User.get_one(user_tg_id)
    full_name = user.get("full_name")

    hm = HEALTH_METRICS.get(metric)

    caption_text = as_list(
        Text(Bold(full_name)),
        Text(hm.get("button_text"))
    )
    caption_kwargs = caption_text.as_caption_kwargs()
    caption_kwargs["photo"] = chart_file

    await message.answer_photo(**caption_kwargs)
