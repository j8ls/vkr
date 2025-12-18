import { Telegraf } from "telegraf";

const token = process.env.BOT_TOKEN;
if (!token) throw new Error("BOT_TOKEN is not set");

const adminIdRaw = process.env.ADMIN_CHAT_ID;
if (!adminIdRaw) throw new Error("ADMIN_CHAT_ID is not set");
const ADMIN_CHAT_ID = Number(adminIdRaw);

const bot = new Telegraf(token);

const helloText =
  "К сожалению, данное исследование уже закрыто.\n" +
  "Но вы можете написать свои пожелания и предложения по темам для будущих постов!\n" +
  "Я обязательно их рассмотрю! Просто напишите ваше сообщение здесь!";

const thanksText = "Спасибо за предложение! Сообщение направленно админу";

function formatUser(ctx: any) {
  const from = ctx.from;
  const fullName = [from?.first_name, from?.last_name].filter(Boolean).join(" ").trim();
  const username = from?.username ? `@${from.username}` : "(без username)"; // username может отсутствовать [web:25]
  const id = from?.id;

  return [
    "Новое сообщение в бот:",
    `Имя: ${fullName || "(без имени)"}`,
    `Username: ${username}`,
    `User ID: ${id}`,
  ].join("\n");
}

bot.start(async (ctx) => {
  await ctx.reply(helloText);
});

bot.on("message", async (ctx) => {
  if (!ctx.chat || ctx.chat.type !== "private") return;
  if (ctx.from?.id === ADMIN_CHAT_ID) return;

  // 1) сначала “шапка” с данными пользователя (имя/username/id) [web:25]
  await ctx.telegram.sendMessage(ADMIN_CHAT_ID, formatUser(ctx));

  // 2) затем форвард исходного сообщения (любой тип: текст/фото/файл) [web:1]
  await ctx.telegram.forwardMessage(
    ADMIN_CHAT_ID,
    ctx.chat.id,
    ctx.message.message_id
  );

  // 3) ответ пользователю
  await ctx.reply(thanksText);
});

bot.launch();

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));
